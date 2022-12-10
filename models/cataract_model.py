import cv2
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from abstract_class import Image,Model
class cataract(Image, Model):
   
   def __init__(self,image):
      self.model = self.create_model()
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

   def prediction(self,weights_path):
      self.model.build((None,224,224,3))
      self.model.load_weights(weights_path)
      return self.model.predict(self.x).argmax(axis=1)
      
