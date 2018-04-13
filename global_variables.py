'''
global_variables.py

File containing all the useful variables. I Tried to have a minimal version as compared to RenderForCNN's global variables.
'''

import pickle
import os

# The base directory, where global_variables.py is situated.
#BASE_DIR = '/home/jogendra/aditya/final_flying_furnitures'
BASE_DIR = '/home/aditya/projects/flying_furniture'

# The Additional Information regarding this dataset. Run save_info.py first.
obj_class = pickle.load(open(os.path.join(BASE_DIR,'info.npy'),'rb'))

# Location for saving the dataset
save_root = os.path.join(BASE_DIR,'data/')

# Additional variables about render lims here

# Light Variables
g_syn_light_num_lowbound = 4
g_syn_light_num_highbound = 8
g_syn_light_dist_lowbound = 9
g_syn_light_dist_highbound = 20
g_syn_light_azimuth_degree_lowbound = 0
g_syn_light_azimuth_degree_highbound = 360
g_syn_light_elevation_degree_lowbound = -45
g_syn_light_elevation_degree_highbound = 45
g_syn_light_energy_mean = 2
g_syn_light_energy_std = 2
g_syn_light_environment_energy_lowbound = 0
g_syn_light_environment_energy_highbound = 1
g_image_size=112

# system Variables:
g_blank_blend_file_path = os.path.join(BASE_DIR,'render_pipeline/blank.blend')
g_save_file_location = os.path.join(BASE_DIR,save_root,'render')
g_save_file_location_final = os.path.join(BASE_DIR,save_root,'render_final')
g_shape_file_location = os.path.join(BASE_DIR,'dataset/ShapeNetCore.v1/')
g_syn_bkg_folder = os.path.join(BASE_DIR,'dataset/SUN2012pascalformat/JPEGImages/')
g_syn_bkg_filelist = os.path.join(BASE_DIR,'dataset/SUN2012pascalformat/filelist.txt')
# where to save the test file list
g_file_list_loc = os.path.join(BASE_DIR,save_root, 'classification/test_list/')
# where to save the test file ground truth
g_test_gt_loc = os.path.join(BASE_DIR,save_root,'classification/test_gt')

# ------------------------------------------------------------
g_blender_executable_path = 'blender' #!! MODIFY if necessary
g_matlab_executable_path = 'matlab' # !! MODIFY if necessary

# ------------------------------------------------------------
# for segmentation
g_clas_file_location = os.path.join(BASE_DIR,save_root,'classification/')
g_seg_file_location = os.path.join(BASE_DIR,save_root,'segmentation/')
g_seg_file_init_location = os.path.join(BASE_DIR,save_root,'segmentation/render')




