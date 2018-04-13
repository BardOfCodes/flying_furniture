#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
CROP_ALL_IMAGES
@brief:
    crop all rendered images of PASCAL3D 12 rigid object classes
'''

import os
import sys
import socket

from global_variables import *
g_save_file_location_cropped = g_save_file_location[:-1] + '_crop/'
g_save_file_location_bkg_overlayed = g_save_file_location[:-1] + '_bkg_overlayed/'
if __name__ == '__main__':
    if not os.path.exists(g_save_file_location_bkg_overlayed):
        os.mkdir(g_save_file_location_bkg_overlayed) 
        
    matlab_cmd = "overlay_background('"+g_save_file_location_cropped+"',"+"'"+g_save_file_location_bkg_overlayed+"','"+g_syn_bkg_filelist+"','"+g_syn_bkg_folder+"');"
    print(matlab_cmd)
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
print('Overlay Done!')

# Final Format
#os.system('mv '+ g_save_file_location_cropped + ' ' + g_save_file_location)
#os.system('rm -rf '+ g_save_file_location)