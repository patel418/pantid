from __future__ import absolute_import
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sys
import glob
import os
import cv2
import numpy as np
import tensorflow as tf
#print ("tensorflow v:" + tf.__version__)
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers.normalization import BatchNormalization
from keras.layers import Dropout
#!conda install --yes --prefix {sys.prefix} opencv
#!{sys.executable} -m pip install opencv-contrib-python
#conda install -c conda-forge opencv


# import sys
# !conda install --yes --prefix {sys.prefix} keras
# 
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
		ret_l.append(new_im)
	return np.array(ret_l)


def find(obj, l, y):
	dir1 = "/Users/Simron/ds/examples/pants/proj/images/" + obj
	   
	    
	#for x in os.walk(dir1):
		    #print 
		    
	m_dir= glob.glob(dir1 + "/*/*jpg")
	print obj
	for files in m_dir:
		image = cv2.imread(files, 1)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		l.append(image)
	l = np.array(l)
	return l
 
# In[2]:
def run():
	os.environ['KMP_DUPLICATE_LIB_OK']='True'


	#images = []

	skinny_j = []
	straight_j = []
	bootc = []
	   
	bootc = find("bc", bootc, 0)
	#print bootc[0].shape
	skinny_j = find("skinny", skinny_j, 1)
	straight_j = find("straight", straight_j, 2)

	y_bc = np.full((bootc.shape[0], 1), 0)
	y_skj = np.full((skinny_j.shape[0], 1), 1)
	y_sj = np.full((straight_j.shape[0], 1), 2)



	# All of the images come of different shapes and sizes so rather than downsampling certain images and risking the loss of data, we will resize and pad certain images and compare which is better. Converted images to grayscale because it took very long

	# In[3]:


	#730 x 480


	# In[4]:


	bootc_r = resize(bootc, 480)
	#print bootc_r[0].shape


	# In[5]:


	skinny_r = resize(skinny_j, 480)
	straight_r = resize(straight_j, 480)


	# In[6]:

	print ("resize")


	X = np.vstack([bootc_r, skinny_r, straight_r])
	y = np.vstack([y_bc, y_skj, y_sj])

	X2 = X
	y2 = y

	print ("stacked")
	#print ("x shape:" + X.shape)
	#print ("y shape:" + y.shape)


	# Now we shall normalize the data by subtracting the mean of the samples from each sample. Additionally we will divide by the standard deviation of each pixel. Subtracting the mean centers the input to 0, and dividing by the standard deviation makes any scaled feature value the number of standard deviations away from the mean.

	# In[7]:



	X2 = X - np.mean(X, axis=0)


	# In[8]:

	print ("mean")

	X2 = X2/np.std(X2, axis=0)


	# In[9]:
	print ("std")


	X_tr, X_t, y_tr, y_t = train_test_split(X2, y, test_size=0.3) 

	print ("tts")
	# In[10]:


	model = Sequential()
	#Convolution
	model.add(Conv2D(32, (3, 3), input_shape = (480, 480, 1), activation = 'relu'))

	#Pooling
	model.add(MaxPooling2D(pool_size = (2, 2)))
	#model.add(BatchNormalization())
	#model.add(Dropout(0.1))
	# Adding a second convolutional layer
	model.add(Conv2D(32, (3, 3), activation = 'relu'))
	model.add(MaxPooling2D(pool_size = (2, 2)))
	# Flattening
	model.add(Flatten())
	model.add(BatchNormalization())
	model.add(Dropout(0.1))
	
	# Full connection
	model.add(Dense(units = 64, activation = 'relu'))
	model.add(Dense(units = 6, activation = 'sigmoid'))
	model.add(Dense(3, activation='softmax'))


	# Compiling the CNN
	model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])


	# In[11]:

	print ("CNN")

	X_tr = np.resize(X_tr, (X_tr.shape[0], X_tr.shape[1], X_tr.shape[2], 1))
	#model.fit(X_tr, y_tr, shuffle=True, epochs=150)


	print("Train Resize")
	# In[1]:


	model.fit(X_tr, y_tr, shuffle=True, epochs=3, batch_size=256)

	print ("FIT")
	# In[ ]:


	X_t = np.resize(X_t, (X_t.shape[0], X_t.shape[1], X_t.shape[2], 1))
	print ("Test Resize")
	score = model.evaluate(X_t, y_t)

	# In[ ]:

	print "hello1"
	print score

	return score

