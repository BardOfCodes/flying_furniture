import sys
import pickle
import os
import time
sys.path.insert(0,'..')
from global_variables import *

# Create the folders for the dataset
if not os.path.exists(g_save_file_location): os.mkdir(g_save_file_location)
# Now we need to call the blender script multiple times,keeping track of the number of files
count_till_prev_class = 0
for iter,(name,obj) in enumerate(obj_class.iteritems()):
    print('Rendering for',name)
    count= 0
    im_num =0
    total_count = 10#obj[4]
    while(count<total_count):
        shape_location = os.path.join(g_shape_file_location,obj[0],obj[3][count%len(obj[3])],'model.obj')
        command = 'blender ' + g_blank_blend_file_path+' --background --python blender_render.py -- '+ g_save_file_location + ' ' + name+' '+ str(im_num) +' '+shape_location
        print(command)
        os.system(command)
        im_num = len(os.listdir(g_save_file_location))
        count = im_num - count_till_prev_class
        #time.sleep(1)
        #asd
    count_till_prev_class = len(os.listdir(g_save_file_location))
print('Render Finish!!')
print('Total Files Rendered:',count_till_prev_class)
        
