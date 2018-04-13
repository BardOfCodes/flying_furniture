'''
process_images.py

File for cropping the rendered images and overlaying some background on them.
Additionally, we save the segmentation maps for the models.
'''

import os 
import sys
import cv2
import random
import numpy as np
from global_variables import *


if __name__ == '__main__':
    if not os.path.exists(g_save_file_location_final):
        os.mkdir(g_save_file_location_final)
    if not os.path.exists(g_seg_file_location):
        os.mkdir(g_seg_file_location)
    # for all the files in g_save_file_location, crop, then overlay, then save in g_save_file_location_final
    all_img = os.listdir(g_save_file_location)
    all_bg = open(g_syn_bkg_filelist).readlines()
    #all_img = [os.path.join(g_save_file_location,x) for x in all_img]
    for iter,img_name in enumerate(all_img):
        print(img_name)
        if iter%len(all_bg) ==0:random.shuffle(all_bg)
        if iter%100 ==0: print('cur iter', iter,'from', len(all_img) )
        img = cv2.imread(os.path.join(g_save_file_location,img_name) , cv2.IMREAD_UNCHANGED) # to read 4 channel
        im = img[:,:,3] # now its 0,1
        im_0 = np.sum(im, axis = 1)
        im_0 = np.cumsum(im_0)
        im_1 = np.sum(im,axis = 0)
        im_1 = np.cumsum(im_1)
        ax_0_start = np.max(np.where(im_0 == im_0[0]))
        ax_0_stop = np.min(np.where(im_0 == im_0[-1]))
        ax_1_start = np.max(np.where(im_1 == im_1[0]))
        ax_1_stop = np.min(np.where(im_1 == im_1[-1]))
        # Now add random noise
        noise = np.random.normal(0,0.0,size = (4))
        ax_0_size = ax_0_stop - ax_0_start
        ax_1_size = ax_1_stop - ax_1_start
        
        leftnew = np.clip(ax_1_start + noise[2]* ax_1_size ,0,im.shape[1])
        rightnew = np.clip(ax_1_stop + noise[3]* ax_1_size ,0,im.shape[1])
        if leftnew > rightnew: leftnew,rightnew = ax_1_start,ax_1_stop
        
        topnew = np.clip(ax_0_start + noise[0]* ax_0_size ,0,im.shape[0])
        bottomnew = np.clip(ax_0_stop + noise[1]* ax_0_size ,0,im.shape[0])
        if topnew > bottomnew: topnew,bottomnew = ax_0_start,ax_0_stop

        left = int(leftnew)
        right = int(rightnew)
        top = int(topnew)
        bottom = int(bottomnew)
        new_img = img[top:bottom, left:right, :]
        new_h,new_w,_ = new_img.shape
        
        
        alpha = np.ceil(new_img[:,:,3]/255.0)
        alpha = np.stack([alpha,]*3,2) 
        seg_map = np.copy(alpha)
        
        # save segmentation? 
        im_class = '_'.join(img_name.split('_')[:-1])  
        color = obj_class[im_class][-1] 
        seg_map[seg_map[:,:,0]>0]= color
        new_name = '.'.join([img_name.split('.')[0],'png'])
        save_file = os.path.join(g_seg_file_location,new_name)
                
        
        if new_h>new_w:
            ratio = g_image_size/float(new_h)
        else:
            ratio = g_image_size/float(new_w)
        # Now cv2 resize according to ratio #for coords too
        new_img = cv2.resize(new_img, (int(ratio*new_w), int(ratio*new_h)), interpolation = cv2.INTER_NEAREST)
        alpha = cv2.resize(alpha, (int(ratio*new_w), int(ratio*new_h)), interpolation = cv2.INTER_NEAREST)
        seg_map = cv2.resize(seg_map, (int(ratio*new_w), int(ratio*new_h)), interpolation = cv2.INTER_NEAREST)
        # Resize the coords too
        #img_coords = ratio*img_coords
        # Now pad the image
        new_h,new_w,_ = new_img.shape
        pad_h = (g_image_size-new_h)
        pad_h_start = pad_h//2
        pad_h_stop = pad_h - pad_h_start
        pad_w = (g_image_size-new_w) 
        pad_w_start = pad_w//2
        pad_w_stop = pad_w - pad_w_start
        new_img= cv2.copyMakeBorder(new_img,pad_h_start,pad_h_stop,pad_w_start,pad_w_stop,cv2.BORDER_CONSTANT,value=0)
        alpha= cv2.copyMakeBorder(alpha,pad_h_start,pad_h_stop,pad_w_start,pad_w_stop,cv2.BORDER_CONSTANT,value=0)
        seg_map= cv2.copyMakeBorder(seg_map,pad_h_start,pad_h_stop,pad_w_start,pad_w_stop,cv2.BORDER_CONSTANT,value=0)
        # now, we need to overlay background
        
        # we should overlay background berfore resize and padding ? No
        
        new_h,new_w,_ = new_img.shape
        kter = 0
        while True:
            bg = cv2.imread(os.path.join(g_syn_bkg_folder,all_bg[(iter+kter) %len(all_bg)].strip() ))
            if bg.shape[0]<new_h+1 or bg.shape[1] < new_w+1 or len(bg.shape)<3:
                kter+=1
            else:
                break
        # now overlay bg
        start_bg_h = np.random.choice(np.arange(bg.shape[0]-new_h))
        start_bg_w = np.random.choice(np.arange(bg.shape[1]-new_w))
        new_bg = bg[start_bg_h:start_bg_h+new_h, start_bg_w:start_bg_w+new_w,:]
        new_img = new_img[:,:,:3]
        new_img  = new_img*alpha + new_bg*(1-alpha) 
        
        
        # now we can save the image
        cv2.imwrite(os.path.join(g_save_file_location_final,img_name), new_img)
        cv2.imwrite(save_file,seg_map)   
        
