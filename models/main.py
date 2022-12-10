from cataract_model import cataract
from diabetic_retinopathy_model import diabetic_retinopathy
import cv2
import os 

'''
A class for checkup it calls the model for prediction of diseases
'''
class Checkup:

    def __init__(self,image_path):
        self.image = cv2.imread(image_path)
        self.image_path = image_path
        #categories consist of the disease and where it's present or not
        self.categories = { "CATARACT": 0,
                            "DIABETIC RETINOPATHY": 0,
                            "AMD": 0,
                            "Glucama":0}
        self.diabetic_retinopathy_classes = { "No DR":0, "Mild NPDR":1, "Moderate NPDR":2, "Severe NPDR":3, "PDR":4, "Ungradable":5}
    
    def call_model(self):
        '''
        Calls the model for prediction
        and then updates the categories dictionary
        '''
        cataract_pred = cataract(self.image).prediction("/home/ayush/Documents/Machine_learning/INFYUVA/final/weights/model_k.h5")
        if cataract_pred[0] == 1:
            self.categories["CATARACT"] = 1
        diabetic_retinopathy_pred = diabetic_retinopathy(self.image).prediction("/home/ayush/Documents/Machine_learning/INFYUVA/final/weights/CL_MULTI_effnetb0-16-0.005-SGD.pt")
        #to get the severity of diabetic retinopathy
        for key, value in self.diabetic_retinopathy_classes.items():
            if value == diabetic_retinopathy_pred:
                self.categories["DIABETIC RETINOPATHY"] = key

    def show_categories(self):
        print(self.categories)

def main():
    obj = Checkup("/home/ayush/Documents/Machine_learning/INFYUVA/cataract_/dataset/1_normal/NL_006.png")
    obj.call_model()
    obj.show_categories()

if __name__ == "__main__":
    main()