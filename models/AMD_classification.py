import numpy as np
from matplotlib import pyplot as plt
import torch
import torchvision
import torch.nn as nn
import torchvision.models as models
from efficientnet_pytorch import EfficientNet
from torchvision.io.image import read_image
from torchvision.transforms.functional import resize


class macular_degeneration():
    def __init__(self, image_path):
        self.IMAGE_PATH = image_path
        self.IMG_DIM = 512
        self.macular_degeneracy_classes = {0: 'Normal', 1 : 'Mild', 2: 'Severe'}
        
    def create_model(self):
        self.weights_path = '/home/ayush/Documents/Machine_learning/INFYUVA/final/weights/AMD.pt'
        self.model = EfficientNet.from_pretrained('efficientnet-b3', num_classes = len(self.macular_degeneracy_classes))
        self.model.load_state_dict(torch.load(self.weights_path, map_location = torch.device('cpu')))
        self.model.to(torch.device('cpu'))
        self.model = self.model.eval()
        return self.model
    
    def show_image(self):
        plt.imshow(self.IMAGE_PATH)
    
    def preprocess_image(self):
        self.image = read_image(self.IMAGE_PATH)
        self.input_tensor = resize(self.image, (self.IMG_DIM, self.IMG_DIM)) / 255.0
        
        return self.input_tensor

    def prediction(self):
        self.model = self.create_model()
        self.input_tensor = self.preprocess_image()
        self.x = self.model(self.input_tensor.unsqueeze(0))

        # return self.model(self.out).argmax().item()
        return self.macular_degeneracy_classes[self.x.argmax().item()]
        # print(self.macular_degeneracy_classes[self.x.argmax().item()])

# def main():
#     macular_degeneration('/home/sid009/jupyter/Infyuva_repo/Infyuva_GITHUB/images/2_glaucoma/Glaucoma_001.png')

# if __name__ == '__main__':
#     main()