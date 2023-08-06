#######################################################################
#### This should be run AFTER the "acquire_image_set" file is run #####
#### so that the correct model and microscope parameters are used  ####
#######################################################################

from nion.utils import Registry
from nion.data import xdata_1_0 as xd

import math
import numpy as np
from time import sleep
from scipy import interpolate
from scipy import ndimage
from skimage.transform import resize
from skimage import io
from sklearn.model_selection import train_test_split
from skimage import draw

from typing import Dict, List, Tuple, Type, Union
from skimage import data, feature, exposure
import os
from copy import deepcopy as dc

import torch
import atomai as aoi
from atomai.utils import (cv_thresh, find_com, get_downsample_factor,
                          get_nb_classes, img_pad, img_resize, peak_refinement,
                          set_train_rng, torch_format_image,
                          torch_format_spectra, graphx)

#############################################
microscope = "home"
ensemblefile  = "new_ensemble_metadict.tar"
#############################################

if microscope == "US100":
    os.chdir("E:/Kevin/!Scripts/ELIT")            # For US100
elif microscope == "US200":
    os.chdir("D:/ASUser/Documents/Kevin/!Scripts/ELIT")   # For US200
elif microscope == "home":
    os.chdir("C:/Users/8kr/Dropbox (ORNL)/Microscopy Data KMR/ELIT")

def grab_frame(field_of_view = 4, size = (50,50), pixeltime = 8, save = True, title = "HAADF"):
  time.sleep(0.1)
  if scan.is_playing is True:
    scan.grab_next_to_finish()[0]
  superscan.stop_playing()
  # print('grabbing frame...')
  frame_params = scan.get_record_frame_parameters()
  frame_params.fov_nm = field_of_view
  frame_params.size = size
  frame_params.pixel_time_us = pixeltime
  frame_params.ac_line_sync = False
  scan.set_record_frame_parameters(frame_params)
  # Setting with profile by index seems to work more reliably... ?
  frame_params_SS = superscan.get_frame_parameters_for_profile_by_index(2)  # index 2 is record, index 0 is puma, etc.
  frame_params_SS['fov_nm'] = field_of_view
  frame_params_SS['size'] = size
  frame_params_SS['pixel_time_us'] = pixeltime
  frame_params_SS['ac_line_sync'] = False
  superscan.set_frame_parameters_for_profile_by_index(2, frame_params_SS)
  # superscan.set_record_frame_parameters(frame_params_SS)
  frame = superscan.record()[0] 
  if save == True:
    frame_data = api.library.create_data_item_from_data_and_metadata(frame, title=title)
    return frame, frame_data
  else:
    return frame

def cross_image(image1, image2): #TODO: make sure the shift in y and x are correct on the scope!
  """
  Determines the shift in pixels from image1 to image2.

  :param image1: first image
  :param image2: second image
  :return: shift in pixels, [yShift,xShift]
  """
  image1FFT = np.fft.fft2(image1)
  image2FFT = np.conjugate(np.fft.fft2(image2))
  imageCCor = np.real(np.fft.ifft2((image1FFT * image2FFT)))
  imageCCorShift = np.fft.fftshift(imageCCor)
  row, col = image1.shape
  yShift, xShift = np.unravel_index(np.argmax(imageCCorShift), (row, col))
  yShift -= int(row / 2)
  xShift -= int(col / 2)
  return yShift, xShift

# def gmm_classify(coord_dict_pred, imgdata, method="gmm_local", n_components=2, window_size=48, coord_class=0):
#   coordinates = aoi.stat.update_classes(coord_dict_pred, imgdata, method=method,
#     n_components=n_components, window_size=window_size, coord_class=coord_class) # other methods: kmeans, meanshift, threshold
#   return coordinates

def atom_classify(coord_dict_pred, imgdata, method="gmm_local", n_components=2, window_size=48, coord_class=0, thresh = 0.5):
  coordinates = aoi.stat.update_classes(coord_dict_pred, imgdata, method=method,
    n_components=n_components, window_size=window_size, coord_class=coord_class, thresh = thresh) # other methods: kmeans, meanshift, threshold
  return coordinates

def normalize(image):
  return (image - np.min(image))/np.ptp(image)

def get_neighbormean(imgarr,coordinate):
  a1,a2,_ = coordinate
  all_c = np.zeros((3**2,2)).astype(int)
  all_c[0,:] = a1-1,a2+1
  all_c[1,:] = a1,  a2+1
  all_c[2,:] = a1+1,a2+1
  all_c[3,:] = a1-1,a2
  all_c[4,:] = a1,a2
  all_c[5,:] = a1+1,a2
  all_c[6,:] = a1-1,a2-1
  all_c[7,:] = a1,a2-1
  all_c[8,:] = a1+1,a2-1

  imgarr = normalize(imgarr)
  ints = []
  for cc in all_c:
    ints.append(imgarr[cc[0],cc[1]])
  ints = np.asarray(ints)

  return np.mean(ints)

def separate_atoms_graphene(imagedata, coordinates, winsizefraction = 0.07, int_range_thresh = 0.4, method = 'gmm_local', good_ratio = 0.1):
  int_range = imagedata.max() - imagedata.min()
  if int_range < int_range_thresh:
    n_comps = 1
  elif int_range > int_range_thresh:
    n_comps = 2

  if n_comps == 1: # It means there are NO amorphous or dopant atoms, therefore everything belongs to lattice and we are done.
    lattice_coords = deepcopy(coordinates)
  else:
    coordinates = atom_classify(coordinates, imagedata, 
                  method = method,
                  n_components = n_comps, 
                  window_size = 1+ int(winsizefraction*d1))  # 5-10% seems ok?

    coords1, coords2 = np.empty((0,2)), np.empty((0,2))

    for ii,c in enumerate(coordinates[0]):
      c1,c2,c3 = c
      if c3 == 0:
        coords1 = np.append(coords1, [c1,c2])
      if c3 == 1:
        coords2 = np.append(coords2, [c1,c2])
    coords1 = coords1.reshape(-1,2)
    coords2 = coords2.reshape(-1,2)
    Lc1, Lc2 = len(coords1), len(coords2)

    L_all = [Lc1,Lc2]
    all_coords = [coords1, coords2]

    L_min = np.argmin(L_all)
    L_tot = np.sum(L_all)

    if L_all[L_min]/L_tot < good_ratio:  # means it was successfully separated - probably...
      amorphous_coords = np.copy(all_coords[L_min])
      lattice_coords = np.copy(all_coords[int(L_min-1)])
    else:
      lattice_coords = np.concatenate((coords1, coords2), axis=0)
      amorphous_coords = np.empty((0,2))

  coords = dc(lattice_coords)         ## this basically ignores amorphous coords for now. I don't think we really want them!
  print("lattice atoms: {}".format(lattice_coords.shape[0])), print("amorphous coords: {}".format(amorphous_coords.shape[0]))

  return coords

def do_ring_search(coords, labeled_img, pixel_conversion = px2ang, rings = rings, defectcolors = defectcolors, radius_ring = radius_def1):
  print("Sniffing for rings..")

  map_dict = {0: "C", 1: "Si"}  # classes to chemical elements. For the moment, silicon is NOT USED

  updatedcoords = dc(coords)
  updatedcoords[:,:2] *= pixel_conversion
  z = np.zeros((updatedcoords.shape[0],1))
  updatedcoords = np.append(updatedcoords, z, axis=1)

  ring_coords = {}

  for ii,RING in enumerate(rings):
    print("Searching {}-rings...".format(RING))
    starttime = time.time()

    if interactive.cancelled:
      print('Interrupted by User!')
      scan.probe_position = (safepos[0],safepos[1])
      1/0

    cycles = [RING]

    # while time.time() < starttime + TIMEOUT:
    G = aoi.utils.graphx.Graph(updatedcoords, map_dict)
    G.find_neighbors()
    G.polycount(max_depth=max(cycles))
    G.remove_filled_polygons()
    rl = [sorted([int(v.id) for v in r]) for r in G.rings]
    rl = sorted(rl, key=lambda x: (len(x), x[0], x[1], x[2]))
    detected_rings = [updatedcoords[r] / pixel_conversion for r in rl if len(r) in cycles]
    try:
      detected_rings_mean = np.concatenate([c.mean(0)[None] for c in detected_rings])
    except ValueError:
      detected_rings_mean = []
    print("{} {}-rings detected".format(len(detected_rings_mean), RING))

    ring_coords['{}'.format(RING)] = detected_rings_mean


    for kk,center in enumerate(detect_rings_mean):
      a,b,_ = center
      rr, cc = draw.disk((a,b),radius_ring,shape=labeled_img.shape)
      labeled_img[rr, cc] = defectcolors[ii]

  return ring_coords

def MoS2_coord_split(imagedata, coordinates, winsizefraction = 0.07, sulfur_threshold = 0.225):
  '''
  Idea is to first separate evrything by local GMM clustering. This seems to work well for MoS2,
  as the Mo atoms are generally cleaner (rounder) and larger in size. 
  Then, with the remaining sulfurs, we then split these by intensity thresholding

  Doing this with 2 thresholds (one for Mo / all sulfurs, and one again for S1 and S2) did not 
  work well. Perhaps some of the double sulfurs' intensity can match that of Mo. I'm not 
  sure how or why, that doesn't seem to make sense. May need finer tuning with thresholding

  In any case, this route seemed to work quite well.

  Note, trying to extract slight intensity variations with a convolutional neural net is 
  probably not the best approach. These are better at identifying geometric features, 
  not intensities. i.e., we don't have a trained network with 3 (really, 4) classes 
  out of the gate. Instead just a single class of ALL atoms, and refine from there.
  Therefore we have gone with this approach here.
  '''
  separation_01 = aoi.stat.update_classes(coordinates, 
                                          imagedata, 
                                          method="gmm_local", 
                                          n_components = 2,
                                          window_size = 1+ int(winsizefraction*d1))

  C1_ints, C2_ints = [], []

  for coord in separation_01[0]:
      if coord[2] == 0:
        C1_ints.append(get_neighbormean(imagedata, coord))
      elif coord[2] == 1:
        C2_ints.append(get_neighbormean(imagedata, coord))
  C1mean, C2mean = np.mean(C1_ints), np.mean(C2_ints)

  if C1mean > C2mean:
    Mo =  separation_01[0][np.where(separation_01[0][:,2] == 0)]
    S  =  separation_01[0][np.where(separation_01[0][:,2] == 1)]
  else:
    S  =  separation_01[0][np.where(separation_01[0][:,2] == 0)]
    Mo =  separation_01[0][np.where(separation_01[0][:,2] == 1)]

  S[:,2] = 0
  separation_02 = aoi.stat.update_classes(S, 
                                          imagedata, 
                                          method="threshold", 
                                          thresh=sulfur_threshold)

  C1_ints, C2_ints = [], []
  for coord in separation_02[0]:
      if coord[2] == 0:
        C1_ints.append(get_neighbormean(imgdata, coord))
      elif coord[2] == 1:
        C2_ints.append(get_neighbormean(imgdata, coord))
  C1mean, C2mean = np.mean(C1_ints), np.mean(C2_ints)

  if C1mean > C2mean:
    S2 =  separation_02[0][np.where(separation_02[0][:,2] == 0)]
    S1  = separation_02[0][np.where(separation_02[0][:,2] == 1)]
  else:
    S1  = separation_02[0][np.where(separation_02[0][:,2] == 0)]
    S2 =  separation_02[0][np.where(separation_02[0][:,2] == 1)]

  for kk,center in enumerate(Mo):
    a,b,_ = center
    rr, cc = draw.disk((a,b),radius_ring,shape=labeled_img.shape)
    labeled_img[rr, cc] = defectcolors[0]
  for kk,center in enumerate(S1):
    a,b,_ = center
    rr, cc = draw.disk((a,b),radius_ring,shape=labeled_img.shape)
    labeled_img[rr, cc] = defectcolors[1]
  for kk,center in enumerate(S2):
    a,b,_ = center
    rr, cc = draw.disk((a,b),radius_ring,shape=labeled_img.shape)
    labeled_img[rr, cc] = defectcolors[2]

  return Mo, S1, S2

def do_dopant_search(imagedata, labeled_img, coordinates, dopant_thresh, radius_dopant):
  print("Identifying dopants, using threshold of: {}".format(dopant_thresh))

  dopant_coords = np.empty((0,2))

  z = np.zeros((coordinates.shape[0],1))
  coord_ints = coordinates.astype(int)
  coord_ints = np.append(coord_ints, z, axis=1).astype(int)
  for ii,c in enumerate(coord_ints):
    c1,c2,_ = c
    if get_neighbormean(imagedata, c) > dopant_thresh:
      dopant_coords = np.append(dopant_coords, [coordinates[ii,0],coordinates[ii,1]])
  dopant_coords = dopant_coords.reshape(-1,2)
  print("Found {} dopant atoms".format(len(dopant_coords)))

  for ii,center in enumerate(dopant_coords):
    a,b = center.astype(int)
    rr1, cc1 = draw.circle_perimeter(a,b,radius_def2-1,shape=labeled_img.shape)
    rr2, cc2 = draw.circle_perimeter(a,b,radius_def2,  shape=labeled_img.shape)
    rr3, cc3 = draw.circle_perimeter(a,b,radius_def2+1,shape=labeled_img.shape)
    labeled_img[rr1, cc1] = [0,1,0]
    labeled_img[rr2, cc2] = [0,1,0]
    labeled_img[rr3, cc3] = [0,1,0]

  return dopant_coords

def image_stage(image_params = image_parameters,
          ADF_title = "ADF 001", 
          labeled_img_title = "All labels: 001"):

  FOV       = image_params[0]
  size      = (image_params[1],image_params[1])
  pixeltime     = image_params[2]
  resizefactor  = image_params[3]
  powerfactor   = image_params[4]
  modelnumber   = image_params[5]

  newsize     = int(FOV*10/resizefactor)*1  ### REMINDER I ADDED a FACTOR of 2 for 70kV, it seems the scale is off!!

  frame_params = scan.get_record_frame_parameters()
  frame_params.fov_nm = FOV
  frame_params.size = size
  frame_params.pixel_time_us = pixeltime
  scan.set_record_frame_parameters(frame_params)
  print("Grabbing image...")
  frame, frame_data = grab_frame(field_of_view = FOV, size = size, pixeltime = pixeltime, save = True, title = ADF_title)
  data1 = dc(frame.data)
  data1_ = dc(data1)                # data1_ is for drift correction and nothing else
  data1_ = (data1_ - np.min(data1_))**powerfactor # Then probably we don't want to do this powerfactor operation...

  imgdata_r = aoi.utils.cv_resize(data1, (newsize, newsize))
  imgdata = normalize((imgdata_r - imgdata_r.min())**powerfactor)

  frame_params = scan.get_record_frame_parameters()
  if scan.is_playing is True:
    scan.grab_next_to_finish()[0]
  superscan.stop_playing()

  shiftx, shifty = 0, 0
  scan.probe_position = (safepos[0],safepos[1])
  if blanked:
    stem_controller.SetVal("C_Blank",1)

  ##############################
  #### Atom finding is next ####
  ##############################

  # device = 'cpu'
  smodel, ensemble = None, None  # Helps to clear memory maybe?
  smodel, ensemble = aoi.models.load_ensemble(ensemblefile)
  smodel.load_state_dict(ensemble[modelnumber])
  decoded_imgs, coordinates = aoi.predictors.SegPredictor(smodel, use_gpu=GPU).run(imgdata)

  decoded = decoded_imgs[0,:,:,0]

  # New part 01.31.2022, auto select number of comps
##### The question is, is this intensity range method a decent way of auto detection of brighter crap in the image? I think so...

  # Initialize the labeled image object, with decoded image as a base. 
  # This won't be populated with defects/features until after they are found!
  labeled_img = np.zeros((newsize,newsize,3))
  for ii in range(labeled_img.shape[0]):
    for jj in range(labeled_img.shape[1]):
      labeled_img[ii,jj,0] = decoded[ii,jj]
      labeled_img[ii,jj,1] = decoded[ii,jj]
      labeled_img[ii,jj,2] = decoded[ii,jj]

  decoded = (decoded - np.min(decoded))/(np.ptp(decoded))

  
  ### Here, we want to conduct the search for what ever species of defect that is specified.
  ### How to do it seamlessly / general way?

  ### e.g., we'll have a:
  ### 1. lattice/amorphous search, 2. ring search, 3. dopant search, and now 4. MoS2 search.
  ### 


  ####### GRAPHENE ########
  if sample == 'graphene':

    coords = separate_atoms_graphene(imgdata, coordinates, 
                     winsizefraction = winsizefraction, int_range_thresh = 0.4, 
                     method = 'gmm_local', good_ratio = 0.1)
    ring_coords = do_ring_search(coords, labeled_img = labeled_img, pixel_conversion = px2ang, rings = rings, ringcolors = ringcolors, radius_ring = radius_def1)
    dopant_coords = do_dopant_search(imgdata_r, coordinates = coords,
                    labeled_img = labeled_img, 
                    dopant_thresh = dopant_thresh, 
                    radius_dopant = radius_def2)
    blast_coords = {}
    blast_coords['Rings'] = ring_coords
    blast_coords['Dopants'] = dopant_coords
  ###### END GRAPHENE #######
  ## Point is to have the blast_coords at this point.

  if sample == 'generic':

    coords = separate_atoms_graphene(imgdata, coordinates, 
                     winsizefraction = winsizefraction, int_range_thresh = 0.4, 
                     method = 'gmm_local', good_ratio = 0.1)
    dopant_coords = do_dopant_search(imgdata_r, coordinates = coords,
                    labeled_img = labeled_img, 
                    dopant_thresh = dopant_thresh, 
                    radius_dopant = radius_def2)
    blast_coords = {}
    blast_coords['Dopants'] = dopant_coords


  elif sample == 'mos2':

    coords_Mo, coords_S1, coords_S2 = MoS2_coord_split(imgdata, coordinates,
                               winsizefraction = winsizefraction, 
                               sulfur_threshold = sulfur_threshold)

    blast_coords = {}
    blast_coords['Mo'] = coords_Mo
      blast_coords['S1'] = coords_S1
      blast_coords['S2'] = coords_S2


  rgb_ = xd.rgb(labeled_img[:,:,0], labeled_img[:,:,1], labeled_img[:,:,2])
  rgb_item = api.library.create_data_item_from_data_and_metadata(rgb_, title= labeled_img_title)

  ## SET the metadata! ##
  dimensional_calibrations = rgb_item.xdata.dimensional_calibrations

  Metadata = {}
  Metadata['Image parameters'] = {}
  Metadata['Image parameters']['FOV'] = image_parameters[0]
  Metadata['Image parameters']['size'] = image_parameters[1]
  Metadata['Image parameters']['pixel_time_us'] = image_parameters[2]
  Metadata['Image parameters']['Resize factor'] = image_parameters[3]
  Metadata['Image parameters']['Power factor'] = image_parameters[4]
  Metadata['Image parameters']['Model'] = image_parameters[5]
  Metadata['Microscope'] = microscope
  Metadata['Coordinates'] = coords
  Metadata['Blast coordinates'] = blast_coords
  Metadata['GPU'] = GPU
  Metadata['Iterations'] = num_iterations
  Metadata['Drift correction'] = drift_correct
  Metadata['Defect dwell'] = dwell_blast
  Metadata['px2ang'] = px2ang
  Metadata['targets'] = targets
  Metadata['Blast location'] = blast_location
  Metadata['Percent to blast'] = Percent_to_blast
  Metadata['Dopant threshold'] = dopant_thresh
  Metadata['Blast offset'] = offset_blast
  Metadata['Use blanking'] = blanked
  Metadata['Safe position'] = safepos
  Metadata['Ensemble file name'] = ensemblefile

  dimensional_calibrations[0].units = Metadata
  rgb_item.set_dimensional_calibrations(dimensional_calibrations)


  if drift_correct == True:
    print("Checking for drift...")
    # This frame grab should be faster... Actually no, it's inaccurate for graphene if fast! Also, contamination edges jump around!
    frame2, frame_data2 = grab_frame(field_of_view = FOV, size = (d1,d2), pixeltime = pix_dwell, save = True, title = 'ADF drift check')
    data2 = dc(frame2.data)
    data2 = (data2 - np.min(data2))**image_parameters[4]
    shiftx, shifty = cross_image(data1_, data2)
    shiftx_frac, shifty_frac = -shifty/d1, -shiftx/d2

    print("Adjusting to account for drift: x: {}, y: {}".format(shiftx,shifty))
  elif drift_correct == False:
    print("No drift correction, too much dose..")
    shiftx_frac, shifty_frac = 0, 0

  ## direct the beam to this position for a specified dwell time.
  stem_controller.SetVal("C_Blank",0)
  sleep(0.5)

  return blast_coords, imgdata, shiftx_frac, shifty_frac

def blast_stage(targets,
        blast_coordinates, 
        image_data):
  
  if "Dopants" in targets:
    numtoblast = int(Percent_to_blast*len(blast_coordinates['Dopants'])+1)
    print("Blasting {} of {} total dopants".format(numtoblast, len(blast_coordinates['Dopants'])))
    for ii,c in enumerate(blast_coordinates['Dopants'][:numtoblast]):
      if interactive.cancelled:
        print('Interrupted by User!')
        scan.probe_position = (safepos[0],safepos[1])
        1/0
      xx0,yy0 = c
      xx0,yy0 = xx0+offset_blast[1], yy0+offset_blast[0]
      xx=(xx0/image_data.shape[0]) + shifty_frac
      yy=(yy0/image_data.shape[1]) + shiftx_frac
      print("Blasting dopant #{}/{} for {} seconds".format(ii+1,numtoblast,dwell_blast))
      scan.probe_position = (xx,yy)
      sleep(dwell_blast)
    scan.probe_position = (safepos[0],safepos[1])

  if "Fives" in targets:
    numtoblast = int(Percent_to_blast*len(blast_coordinates['Dopants']['5'])+1)
    print("Blasting {} of {} total 5-ring clusters".format(numtoblast, len(blast_coordinates['Dopants']['5'])))
    for ii,c in enumerate(blast_coordinates['Dopants']['5'][:numtoblast]):
      if interactive.cancelled:
        print('Interrupted by User!')
        scan.probe_position = (safepos[0],safepos[1])
        1/0
      xx0,yy0,_ = c
      xx0,yy0 = xx0+offset_blast[1], yy0+offset_blast[0]
      xx=(xx0/image_data.shape[0])+ shifty_frac
      yy=(yy0/image_data.shape[1])+ shiftx_frac
      print("Blasting 5-ring cluster #{}/{} for {} seconds".format(ii+1,numtoblast,dwell_blast))
      scan.probe_position = (xx,yy)
      sleep(dwell_blast)
    scan.probe_position = (safepos[0],safepos[1])

  if "Sevens" in targets:
    numtoblast = int(Percent_to_blast*len(blast_coordinates['Dopants']['7'])+1)
    print("Blasting {} of {} total 7-ring clusters".format(numtoblast, len(blast_coordinates['Dopants']['7'])))
    for ii,c in enumerate(blast_coordinates['Dopants']['7'][:numtoblast]):
      if interactive.cancelled:
        print('Interrupted by User!')
        scan.probe_position = (safepos[0],safepos[1])
        1/0
      xx0,yy0,_ = c
      xx0,yy0 = xx0+offset_blast[1], yy0+offset_blast[0]
      xx=(xx0/image_data.shape[0])+ shifty_frac
      yy=(yy0/image_data.shape[1])+ shiftx_frac
      print("Blasting 7-ring cluster #{}/{} for {} seconds".format(ii+1,numtoblast,dwell_blast))
      scan.probe_position = (xx,yy)
      sleep(dwell_blast)
    scan.probe_position = (safepos[0],safepos[1])

def ELITexperiment(superscan, ensemblefile, sample, image_parameters, px2ang,
                  targets, num_iterations, threshold, winsizefraction,
                  blastdwell, Percent_to_blast, offset_blast,
                  GPU = False,
                  drift_correct = False):


  # interactive = api_broker.get_interactive(version='~1.0')
  # api = api_broker.get_api(version='~1.0')
  # superscan = api.get_hardware_source_by_id('superscan', '1')

  # microscope    = 'MACSTEM'
  # GPU       = True #True  # U200 / MACSTEM can be True, U100 has shit GPU, so False there.
  # use_augmented = True
  # ensemblefile  = "augmented_graphene_ensemble_metadict.tar" # "graphene_ensemble_metadict.tar"

  # GLOBALS 


  # threshold= 0.225   # 0.225 for S1 vs S2, something else for dopants in graphene (like 0.3 or so)
  # winsizefraction = 0.07    # For GMM sorting; fraction of entire image,

  # sample      = 'graphene' #  'graphene', 'generic', 'mos2'  
  # targets     = ['Dopants'] # "Fives" "Sevens" "Dopants".... "Mo", "S1", "S2",.. or defect1, defect2.. hmm
  # num_iterations  = 100             # # times to repeat the img-blast-img sequence. Note, 2 iterations is img-blast-img-blast
  # drift_correct = False             # This can cause a significant amount of dose if we do it
  # RUN THE "acquire_image_set" file FIRST!

  # dwell_blast   = 3               # seconds to blast the defect
  # [FOV in nm, pixel dimensions, dwell time, pix 2 angstrom, img process power factor, model number]

  # image_parameters= [12, 512, 32, 0.18, 1.25, 4]    # For US100 @ 80kV


  # image_parameters= [8, 512, 128, 0.104, 1.5, 4]  # For US200 @ 100kV
  # image_parameters= [6, 512, 128, 0.12, 1.25, 4]    # For US200 @ 80kV    

  # image_parameters= [16, 512, 90, 0.18, 2, 7]   # [FOV in nm, pixel dimensions, dwell time, pix 2 angstrom, img process power factor, model number]
  # TIMEOUT     = 5               # seconds for which if elapsed, defect search is called off

  # px2ang      = 0.12                # 0.12 (0.12 for 100kv, 0.16 for 80kV)        
  # px2ang      = 0.104               # For US200 @ 100 kV, 8nm FOV, and 0.104 pix 2 angstrom, use 0.12                                           
  # px2ang      = 0.080               # US100 @ 70 kV,  0.08      
                          # US100 @ 100 kV, 0.104
                          # Idea is that if topological, then it will blast either/both 5/7s, and if dopant, then only dopant.

 
         # "centroid" or "atom" blast center of mass, or the first atom in the cluster
  # offset_blast  = [0,0]             # [x,y] offset from center coordinate of feature to blast
  # Percent_to_blast= 1               # percentage of defects to blast (0 to 1)
  ### Beam mod parameters

  # dopant_thresh   = 0.45 # 0.25 # 0.17      # [0 to 1]




############ Hard coded for now #############
  rings       = [5,6,7]
  safepos     = [1,1]             # beam park position between processes
  
  blanked     = False             # blanking can be dangerous for blasting gunk around  

  blast_location  = "centroid"   
  ignore_edges  = True              # TO DO/not implemented yet! Basically only consider coordinates away from edges.
                                    # This wont really help with contamination defects though
  ### Drawing parameters                        
  radius_atom = 2
  radius_def1 = 5   # ring defect
  radius_def2 = 10  # dopant
  defectcolors = [[1,1,0], [0,0,1], [0,1,0]]

################################################



  interactive = api_broker.get_interactive(version='~1.0')
  api = api_broker.get_api(version='~1.0')
  superscan = api.get_hardware_source_by_id('superscan', '1')
  stem_controller = Registry.get_component("stem_controller")
  scan = stem_controller.scan_controller
  stem_controller.SetVal("C_Blank",0)

  ## conversions ##
  FOV       = image_parameters[0]
  d1,d2     = image_parameters[1], image_parameters[1]  # HAADF size   # 1024 for FOV 8nm, 512 for FOV 4nm
  pix_dwell     = image_parameters[2]
  resizefactor    = image_parameters[3]
  powerfactor   = image_parameters[4]
  modelnumber   = image_parameters[5]

  # image_parameters= [6, 512, 40, 0.18, 1.75, 4]

  newsize     = int(FOV*10/resizefactor)*1  ### REMINDER I ADDED a FACTOR of 2 for 70kV, it seems the scale is off!!
  nm_per_pix    = FOV / d1

  frame_params = scan.get_record_frame_parameters()
  frame_params.fov_nm = FOV
  frame_params.size = (d1,d2)
  frame_params.pixel_time_us = pix_dwell
  scan.set_record_frame_parameters(frame_params)

  if scan.is_playing is True:
    scan.grab_next_to_finish()[0]
    superscan.stop_playing()

  # is_confirmed = interactive.confirm_yes_no('Make sure dopant or amorphous is in FOV')
  # if is_confirmed == False:
  #   print("No?! Maybe another time then, bro")
  # else:
  #   print("Deploying warheads")

  ############### Begin image-blast sequence of ELIT! ##############

  for ii in range(num_iterations):
    print("Commence iteration #{} of {}".format(ii+1, num_iterations))

    blast_coords, image_data, shiftx_frac, shifty_frac = image_stage(
                image_parameters, 
                ADF_title = "ADF_{}".format(str(ii).zfill(3)),
                  labeled_img_title = "labels_all_{}".format(str(ii).zfill(3)))

    blast_stage(targets = targets, 
          blast_coordinates = blast_coords,
          image_data = image_data)
      
  print("At the end of the road. Turn back, traveler")
  scan.probe_position = (safepos[0],safepos[1])

def ELITscan(api,superscan, window, px2ang, image_process, modelnumber):
  # interactive = api_broker.get_interactive(version='~1.0')
  # api = api_broker.get_api(version='~1.0')
  superscan = api.get_hardware_source_by_id('superscan', '1')   # MICROSCOPE
  superscan = api.get_hardware_source_by_id('usim_scan_device', '1')  # SIMULATOR

  stem_controller = Registry.get_component("stem_controller")
  scan = stem_controller.scan_controller
  stem_controller.SetVal("C_Blank",0)
  # window = api.application.document_windows[0]

  # profile = scan.profile_index # profile_index doesn't exist for scan variable. Probably something ismilar...
  profile = superscan.profile_index
  frame_params = scan.get_frame_parameters(profile)
  FOV = frame_params.fov_nm
  newsize = int(FOV*10/px2ang)

  # FOV, d1, d2, pix_dwell, px2ang, image_process, modelnumber, newsize = get_parameters(image_parameters)

  smodel, ensemble = None, None  # Clear memory maybe?
  smodel, ensemble = aoi.models.load_ensemble(ensemblefile)
  smodel.load_state_dict(ensemble[modelnumber])
  if scan.is_playing is True:
    scan.grab_next_to_finish()[0]
    superscan.stop_playing()
  newframe, _ = grab_ELIT_frame_first(save = True, title = "[Live] ELIT scan")
  # input("Place the library item somewhere and select it. DO NOT SELECT ANYTHING ELSE")

  liveframe = window.target_data_item
  framenum = 0
  while 1 > 0:
    if interactive.cancelled:
      print("Canceled")
      superscan.stop_playing()
      keystroke = input("Press cancel to stop, or Enter to continue")
      if keystroke == None:
        break
    grab_frame_live_and_decode(smodel, newsize, image_process, liveframe, GPU = True)
    framenum +=1
