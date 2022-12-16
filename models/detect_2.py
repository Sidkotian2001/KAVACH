from cataract_model import cataract
from diabetic_retinopathy_model import diabetic_retinopathy
from AMD_classification import macular_degeneration
import cv2
import os
import socket

'''
A class for checkup it calls the model for prediction of diseases
'''
class Checkup:

    def __init__(self):
        # self.image = cv2.imread(image_path)
        # self.image_path = image_path
        #categories consist of the disease and where it's present or not
        self.categories = { "CATARACT": 0,
                            "DIABETIC RETINOPATHY": 0,
                            "Macular Degeneration": 0,
                            "Glucama":0}
        self.diabetic_retinopathy_classes = { "No DR":0, "Mild NPDR":1, "Moderate NPDR":2, "Severe NPDR":3, "PDR":4, "Ungradable":5}
    
    def setup_client(self):
        print("Starting connection")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.273.170', 5000))
        

        # Receive the length of the image data for the first image
        image1_size = int(client_socket.recv(640 * 480 * 3 * 8))

        # Receive the image data for the first image
        print("Getting first image")
        image1_bytes = bytearray()
        while len(image1_bytes) < image1_size:
            image1_bytes += client_socket.recv(640 * 480 * 3 * 8)

        # Convert the image data to a NumPy array
        image1 = cv2.imdecode(image1_bytes, cv2.IMREAD_UNCHANGED)
        print("Received the first image")
        # Receive the length of the image data for the second image
        image2_size = int(client_socket.recv(1024))

        print("Receiving the second image")
        # Receive the image data for the second image
        image2_bytes = bytearray()
        while len(image2_bytes) < image2_size:
            image2_bytes += client_socket.recv(1024)

        # Convert the image data to a NumPy array
        image2 = cv2.imdecode(image2_bytes, cv2.IMREAD_UNCHANGED)
        print("Received second image")
        # Close the connection to the server

        cv2.imwrite('image1.png', image1)
        cv2.imwrite('image2.png', image2)

        client_socket.close()
        

    def call_model(self):
        '''
        Calls the model for prediction
        and then updates the categories dictionary
        '''
        cataract_pred = cataract(self.image).prediction()
        if cataract_pred[0] == 1:
            self.categories["CATARACT"] = 1
        
        diabetic_retinopathy_pred = diabetic_retinopathy(self.image).prediction()
        #to get the severity of diabetic retinopathy
        for key, value in self.diabetic_retinopathy_classes.items():
            if value == diabetic_retinopathy_pred:
                self.categories["DIABETIC RETINOPATHY"] = key
        
        macular_degeneration_pred = macular_degeneration(self.image_path).prediction()
        self.categories['Macular Degeneration'] = macular_degeneration_pred

    def show_categories(self):
        print(self.categories)

def main():
    obj = Checkup()
#     obj = Checkup("/home/ayush/Documents/Machine_learning/INFYUVA/final/images/2_cataract/cataract_004.png")
    obj.setup_client()
    # obj.call_model()
    # obj.show_categories()

if __name__ == "__main__":
    main()