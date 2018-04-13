# Now this file will read the generated files, 
# split for train and test
import sys
sys.path.insert(0,'..')
from global_variables import *
import os
import random
import copy
all_files = os.listdir(g_save_file_location_final)
test_files = []
train_files = []

for iter,(name, obj) in enumerate(obj_class.iteritems()):
    class_files = [x for x in all_files if name in x]
    random.shuffle(class_files)
    test_ = class_files[:obj_class[name][-3]]
    test_ = [x+' '+str(obj_class[name][-2]) for x in test_]
    test_files.extend(test_)
    train_ = class_files[obj_class[name][-3]:]
    train_ = [x+' '+str(obj_class[name][-2]) for x in train_]
    train_files.extend(train_)

# now we have lists with the names and the gt
random.shuffle(train_files)
random.shuffle(test_files)
train_files = test_files[:100]
test_files = test_files[100:]
print(len(train_files))
print(len(test_files))
print(train_files[0])
print(test_files[0])
# Now move them to new location with new name,
# while writing train_file,test_file,test_file_internal(which will remain with the creator)

if not os.path.exists(g_clas_file_location):
    os.mkdir(g_clas_file_location) 
if not os.path.exists(g_test_gt_loc):
    os.mkdir(g_test_gt_loc) 
if not os.path.exists(g_file_list_loc):
    os.mkdir(g_file_list_loc)
    
train_loc = os.path.join(g_clas_file_location,'train/')
if not os.path.exists(train_loc):
    os.mkdir(train_loc) 
test_loc = os.path.join(g_clas_file_location,'test/')
if not os.path.exists(test_loc):
    os.mkdir(test_loc) 
    
seg_train_loc = os.path.join(g_seg_file_location,'train')
if not os.path.exists(seg_train_loc):
    os.mkdir(seg_train_loc) 
seg_test_loc = os.path.join(g_seg_file_location,'test')
if not os.path.exists(seg_test_loc):
    os.mkdir(seg_test_loc) 
    
    
    
f_train = open(os.path.join(g_file_list_loc,'train_list.txt'),'w')
g_train = open(os.path.join(g_save_file_location,'train.txt'),'w')


for iter,file_ in enumerate(train_files):
    file_name,label = file_.split(' ')
    #file_name = file_name.split('.')[0] + '.jpg'
    full_file_name = os.path.join(g_save_file_location_final,file_name)
    new_im = 'image_'+format(iter, '05d')+'.jpg'
    new_file_name = os.path.join(train_loc,new_im)
    os.system('cp '+full_file_name + ' ' + new_file_name)
    #print('cp '+full_file_name + ' ' + new_file_name)
    seg_name = file_name.split('.')[0] + '.png'
    new_im_seg = 'image_'+format(iter, '05d')+'.png'
    # for segmentation
    full_file_name = os.path.join(g_seg_file_init_location,seg_name)
    new_file_name = os.path.join(seg_train_loc,new_im_seg)
    os.system('cp '+full_file_name + ' ' + new_file_name)
    #print('cp '+full_file_name + ' ' + new_file_name)
    g_train.write(new_im_seg + '\n')
        
    f_train.write(new_im + ' ' + label + '\n')
f_train.close()
g_train.close()
count = copy.copy(iter+1)


f_test = open(os.path.join(g_file_list_loc,'test_list.txt'),'w')
f_test_gt = open(os.path.join(g_test_gt_loc,'test_gt.txt'),'w')
g_test = open(os.path.join(seg_test_loc,'test.txt'),'w')
for iter,file_ in enumerate(test_files):
    file_name,label = file_.split(' ')
    #file_name = file_name.split('.')[0] + '.jpg'
    full_file_name = os.path.join(g_save_file_location_final,file_name)
    new_im = 'image_'+format(iter+count, '05d')+'.jpg'
    new_file_name = os.path.join(test_loc,new_im)
    os.system('cp '+full_file_name + ' ' + new_file_name)
    f_test.write(new_im +'\n')
    f_test_gt.write(new_im + ' ' + label + '\n')
    seg_name = file_name.split('.')[0] + '.png'
    new_im_seg = 'image_'+format(iter+count, '05d')+'.png'
    # for segmentation
    full_file_name = os.path.join(g_seg_file_init_location,seg_name)
    new_file_name = os.path.join(seg_test_loc,new_im_seg)
    os.system('cp '+full_file_name + ' ' + new_file_name)
    #print(full_file_name,new_file_name)
    g_test.write(new_im_seg + '\n')
f_test.close()
f_test_gt.close()
g_test.close()

