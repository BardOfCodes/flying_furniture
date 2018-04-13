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
if __name__ == '__main__':
    if not os.path.exists(g_save_file_location_cropped):
        os.mkdir(g_save_file_location_cropped) 
        
    matlab_cmd = "crop_images('"+g_save_file_location+"',"+"'"+g_save_file_location_cropped+"'"+","+str(g_image_size)+");"
    print(matlab_cmd)
    os.system('%s -nodisplay -r "try %s ; catch; end; quit;"' % (g_matlab_executable_path, matlab_cmd))
print('Crop Done!')

# Final Format
#os.system('mv '+ g_save_file_location_cropped + ' ' + g_save_file_location)
#os.system('rm -rf '+ g_save_file_location)