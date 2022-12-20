import cv2
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from models.abstract_class import Image, Model
import tensorflow as tf
import logging, os
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class cataract(Image, Model):
   
   def __init__(self,image):
      # tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
      self.model = self.create_model()
      self.weights_path = '../weights/CATARACT.h5'
      self.model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
      self.image = image
      self.x = None
      self.preprocess_image()

   def show_image(self):
      plt.imshow(self.image)

   def create_model(self):
      '''
      Creates a model for cataract detection
      '''
      model = keras.Sequential()
      model.add(keras.layers.Conv2D(32,3,activation='relu'))
      model.add(keras.layers.MaxPooling2D(2,strides=(2,2)))
      model.add(keras.layers.Conv2D(32,3,activation='relu'))
      model.add(keras.layers.MaxPooling2D(2,strides=(2,2)))
      model.add(keras.layers.Conv2D(64,3,activation='relu'))
      model.add(keras.layers.MaxPooling2D(2,strides=(2,2)))
      model.add(keras.layers.Conv2D(128,3,activation='relu'))
      model.add(keras.layers.MaxPooling2D(2,strides=(2,2)))
      model.add(keras.layers.Flatten())
      model.add(keras.layers.Dense(64,activation='relu'))
      model.add(keras.layers.Dropout(0.4))
      model.add(keras.layers.Dense(128,activation='relu'))
      model.add(keras.layers.Dropout(0.4))
      model.add(keras.layers.Dense(256,activation='relu'))
      model.add(keras.layers.Dropout(0.5))
      model.add(keras.layers.Dense(2,activation='softmax'))
      return model

   def preprocess_image(self):
      '''
      Preprocesses the image for prediction
      '''
      new_array = cv2.resize(self.image,(224,224))
      self.x = np.array(new_array).reshape(-1, 224, 224, 3)
      self.x = self.x.astype('float32')
      self.x = self.x/255

   def prediction(self):
      self.model.build((None,224,224,3))
      self.model.load_weights(self.weights_path)
      with tf.device('/cpu:0'):
         return self.model.predict(self.x).argmax(axis=1)