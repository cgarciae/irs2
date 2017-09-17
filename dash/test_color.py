#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 10:54:09 2017

@author: camilo
"""



from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import numpy as np
from scipy.misc import imsave


def get_main_colors(image_folder, list_images_names, Nmain=3, NUM_CLUSTERS=5):
    
    
    ar=[]
    for j in range(len(list_images_names)):
        im = Image.open(image_folder+list_images_names[j])
        im = im.resize((150, 150))      # optional, to reduce time
        ar1 = scipy.misc.fromimage(im)
        if list_images_names[j].find(".png")>=0:
            ar1=ar1[:,:,0:3]
        shape = ar1.shape
        print(shape)
        ar1 = ar1.reshape(scipy.product(shape[:2]), shape[2])
        ar.append(ar1)
    
    
    
    ar=np.vstack(ar)
    
    codes, dist = scipy.cluster.vq.kmeans(ar.astype(float), NUM_CLUSTERS)

    
    vecs, dist = scipy.cluster.vq.vq(ar.astype(float), codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences
    
    
    
    MainRepeated=counts.argsort()[-Nmain:][::-1]
    
    
    perc=100*counts[MainRepeated]/len(ar)
    
    colors_rep=[]
    for j in range(Nmain):
        colors_rep.append(codes[MainRepeated[j]].astype(int))
        
    print(colors_rep, perc)
    
    return colors_rep, perc    
    


def generate_colormap(colors_rep, size_img=[5,5]):
    for j in range(len(colors_rep)):
        img=np.zeros((size_img[0], size_img[1], 3))
        img[:,:,0]=colors_rep[j][0]
        img[:,:,1]=colors_rep[j][1]
        img[:,:,2]=colors_rep[j][2]
        imsave("./dash/imagecolor"+str(j)+".jpg", img)


if __name__ == '__main__':
    folder_images="/home/camilo/Camilo/BrandonLogan/irs2/data/images2440/imgs/"
    image_files=['52188867f88e5a7657bceaeb008bf0c2.jpeg', 'dribbble_a88126093ff7b6fe02c968bc1ef5c4ae.png', 'dribbble_d0172d20bb91fe8a843ee301c3df58be.jpg']
    
    colors, perc=get_main_colors(folder_images, image_files)
    generate_colormap(colors)
    
    