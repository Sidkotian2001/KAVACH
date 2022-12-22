from models.cataract_model import cataract
from models.diabetic_retinopathy_model import diabetic_retinopathy
from models.AMD_classification import macular_degeneration
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
        self.categories = { "CATARACT": -1,
                            "DIABETIC RETINOPATHY": -1,
                            "Macular Degeneration": -1,
                            "Glucama":-1}
        self.diabetic_retinopathy_classes = { "No DR":0, "Mild NPDR":1, "Moderate NPDR":2, "Severe NPDR":3, "PDR":4, "Ungradable":5}
    
    def call_model(self, cat, dr, md, glaucama):
        '''
        Calls the model for prediction
        and then updates the categories dictionary
        '''
        if cat == True:
            cataract_pred = cataract(self.image).prediction()
            if cataract_pred[0] == 1:
                self.categories["CATARACT"] = 1
            else :
                self.categories["CATARACT"] = 0
        
        if dr == True:
            diabetic_retinopathy_pred = diabetic_retinopathy(self.image).prediction()
            #to get the severity of diabetic retinopathy
            for key, value in self.diabetic_retinopathy_classes.items():
                if value == diabetic_retinopathy_pred:
                    self.categories["DIABETIC RETINOPATHY"] = key
        if md == True:
            macular_degeneration_pred = macular_degeneration(self.image_path).prediction()
            self.categories['Macular Degeneration'] = macular_degeneration_pred

        if glaucama == True:
            self.categories['Glucama'] = 1

    def show_categories(self):
        print(self.categories)

