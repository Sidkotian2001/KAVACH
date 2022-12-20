import torch
import torchvision.models as models
import torch.nn as nn
from torchvision.io.image import read_image
from torchvision.transforms.functional import resize
import cv2
from models.abstract_class import Image,Model
import matplotlib.pyplot as plt
import logging, os
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class diabetic_retinopathy(Image, Model):
    def __init__(self,image):
        self.weights_path = '../weights/DR.pt'
        self.image = image
        self.model = self.create_model()
        self.x = None
        self.preprocess_image()

    def create_model(self):
        '''
        Creates a model for diabetic retinopathy detection
        '''
        model = models.efficientnet_b0(pretrained=True)
        model.classifier[-1] = nn.Linear(in_features=1280, out_features=6)
        return model

    def show_image(self):
        plt.imshow(self.image)

    def preprocess_image(self):
        '''
        Preprocesses the image for prediction
        '''
        new_array = cv2.resize(self.image,(512,512))
        self.x = torch.unsqueeze(torch.tensor(new_array).permute(2,0,1),0).float()
        
    def prediction(self):
        '''
        Predicts the class of the image using the weights
        '''
        self.model.load_state_dict(torch.load(self.weights_path, map_location=torch.device('cpu')))
        self.model = self.model.eval()
        return self.model(self.x).argmax().item()

