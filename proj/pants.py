
# coding: utf-8

# In[37]:

import sys
#!conda install --yes --prefix {sys.prefix} opencv
#get_ipython().system(u'{sys.executable} -m pip install opencv-contrib-python')
#conda install -c conda-forge opencv


# In[20]:

import glob
import os
import cv2
import numpy as np
#images = []

skinny_j = []
straight_j = []
bootc = []
def find(obj, l):
    dir1 = "/Users/Simron/ds/examples/pants/proj/images/" + obj
   
    
    #for x in os.walk(dir1):
            #print x
    m_dir= glob.glob(dir1 + "/*/*jpg")
    for files in m_dir:
            image = cv2.imread(files, 1)
            print image.shape
            
            #print image.shape
            #asp = 100.0 / image.shape[1]
            #dim = (100, int(image.shape[0]*asp))
            
            #resize = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            #print resize.shape
            #l.append(resize)
            l.append(image)
    l = np.array(l)
    #print ("shape:", l.shape)
    return l
    
bootc = find("bc", bootc)
skinny_j = find("skinny", skinny_j)
straight_j = find("straight", straight_j)

y_bc = np.full((bootc.shape[0], 1), 0)
y_skj = np.full((skinny_j.shape[0], 1), 1)
y_sj = np.full((straight_j.shape[0], 1), 2)



# All of the images come of different shapes and sizes so rather than downsampling certain images and risking the loss of data, we will resize and pad certain images and compare which is better.

# In[36]:

#730 x 480

def resize(l, size):
    ret_l = []   
    count = 0
    for i in range(len(l)):        
        o_size = l[i].shape[:2]

        ratio = float(size)/max(o_size)
        n_size = tuple([int(x*ratio) for x in o_size])

        im = l[i]
        im = cv2.resize(im, (n_size[1], n_size[0]))

        delta_w = size - n_size[1]
        delta_h = size - n_size[0]
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)
        color = [0, 0, 0]
        new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        #print new_im.shape
        ret_l.append(new_im)
    #for e in np.array(ret_l):
            #print e.shape
    return np.array(ret_l)


# In[ ]:

bootc_r = resize(bootc, 730)


# In[ ]:

skinny_r = resize(skinny_j, 730)
straight_r = resize(straight_j, 730)


# In[ ]:



X = np.vstack([bootc_r, skinny_r, straight_r])
y = np.vstack([y_bc, y_skj, y_sj])
#print X.shape
#print X[0].shape

#X2 = np.array([])


# In[ ]:

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense


print "keras!!"
# In[ ]:

model = Sequential()
#Convolution
model.add(Conv2D(32, (3, 3), input_shape = (730, 730, 3), activation = 'relu'))

#Pooling
model.add(MaxPooling2D(pool_size = (2, 2)))


# Adding a second convolutional layer
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))


# Flattening
model.add(Flatten())

# Full connection
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 1, activation = 'sigmoid'))

# Compiling the CNN
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# ### 
