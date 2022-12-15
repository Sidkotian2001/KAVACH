import numpy as np
import cv2 as cv
import mediapipe as mp
import math
from playsound import playsound
import time
import multiprocessing


class iris_voice():
    def __init__(self):
        # self.cap = cv.VideoCapture(0)
        self.is_eye_in_square = False
        self.frame_original = None

        self.shared_variable = multiprocessing.Value('i')
        self.shared_eye_count = multiprocessing.Array('i', 2)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.distances = []
        self.focii = []
        self.message = None
        self.colour = None

        #Landmark numbers for each part of the eyes
        self.LEFT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
        self.RIGHT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        self.LEFT_IRIS = [469, 470, 471, 472]
        self.RIGHT_IRIS = [474, 475, 476, 477]
        self.CENTERS = [468, 473]
        self.shared_eye_count[0] = 0
        self.shared_eye_count[1] = 0

    def mediapipe_detection(self, image, face):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = face.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        return image, results

    #Focal length calculations for the web camera 

    #focal length for distance = 70cm is 611cm
    #focal length for distance = 60cm is 618cm
    #focal length for distance = 50cm is 602cm
    #focal length for distance = 40cm is 610cm

    #AVERAGE FOCAL LENGTH = 610.25cm

    def get_distance(self, coord1, coord2):
        
        dist_btwn_irises_in_pixels = math.dist(coord1, coord2)
        dist_btwn_irises_in_cm = 7
        face_dist_in_cm = 80
        avg_focal_length = 610
        
        focal_length = (dist_btwn_irises_in_pixels * face_dist_in_cm) / dist_btwn_irises_in_cm
        self.focii.append(focal_length)
        
        
        actual_distance = (avg_focal_length * dist_btwn_irises_in_cm) / dist_btwn_irises_in_pixels
        self.distances.append(actual_distance)

    def part_detection(self, part, facial_landmarks, image_shape):
        idx_to_coordinates = {}
        img_height, img_width, _ = image_shape
        for idx, landmark in enumerate(part):
            coord = facial_landmarks.landmark[landmark]
            
            p_x = min(math.floor(coord.x * img_width), img_width - 1)
            p_y = min(math.floor(coord.y * img_height), img_height - 1)
            landmark_coord = (p_x, p_y)
            
            if landmark_coord:
                idx_to_coordinates[idx] = landmark_coord
        return idx_to_coordinates


    def display_part(self, image, coords, color, show_landmarks = False, pupils_coords = False):
        points = np.zeros(shape = (len(coords), 2))
        for idx, landmark_px in coords.items():
            points[idx] = landmark_px
            if show_landmarks == True:
                cv.circle(image, landmark_px, 1, (255, 0, 0), 2)
        points = points.astype(np.int32)
        
        #Only for center coordinates
        if pupils_coords == False:
            cv.polylines(image, [points], True, color, 2)

    def create_coordinates_array(self, x1, y1, x2, y2):
        arr = []
        for i in range(x1, x2):
            for j in range(y1, y2):
                arr.append((i,j))
        return arr

    #Play the voice command at particular intervals
    def play_sound(self):
        msgs = ['Go left', 'Go right', 'Go up', 'Go down', 'Get closer', 'Go Farther', 'Stay in Square']
        if self.shared_variable.value != -1:
            print("sound:", msgs[self.shared_variable.value])
            playsound("Voice_commands/{}.mp3".format(msgs[self.shared_variable.value]))
                

    def correct_position(self, image, pupils_coords, left_iris_coords, right_iris_coords, number_of_eyes_captured):
        
        #Voice commands
        voice_commands = ['Go left', 'Go right', 'Go up', 'Go down', 'Get closer', 'Go Farther', 'Stay in Square']
        
        #Getting the distances
        upper_dist = 50
        lower_dist = 10
        actual_dist = self.distances[-1]

        if number_of_eyes_captured == 0:
            #Left pupil coordinates
            pupil_x = pupils_coords[0][0]
            pupil_y = pupils_coords[0][1]

            #Left iris coordinates
            iris_right = left_iris_coords[0]
            iris_top = left_iris_coords[1]
            iris_left = left_iris_coords[2]
            iris_bottom = left_iris_coords[3]

        elif number_of_eyes_captured == 1:
            #Right pupil right coordinates
            pupil_x = pupils_coords[1][0]
            pupil_y = pupils_coords[1][1]

            #Right iris coordinates
            iris_right = right_iris_coords[0]
            iris_top = right_iris_coords[1]
            iris_left = right_iris_coords[2]
            iris_bottom = right_iris_coords[3]   
        
        elif number_of_eyes_captured > 1:
            #Both the eyes are localized exiting
            print("correct position : Both the eyes are localized, finished image capture")
            cv.putText(image, "correct_position : both the eyes are localized, finished image capture", (200, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
            # exit()
        
        #Center rectangle coordinates
        center_x1, center_y1 = 300, 210
        center_x2, center_y2 = 340, 270

        arr = self.create_coordinates_array(center_x1, center_y1, center_x2, center_y2)
        
        #Check if eyes are in rectangles
        if  (iris_right in arr) and (iris_left in arr) and (iris_top in arr) and (iris_bottom in arr):
            #voice command = "Go Farther"
            if actual_dist > upper_dist:
                self.shared_variable.value = 4
                colour = (0, 0, 255)
            
            #voice command = "Get Closer"
            elif actual_dist < lower_dist:
                self.shared_variable.value = 5
                colour = (0, 255, 0)
            
            #voice command = "Stay in Square"
            else:
                self.shared_variable.value = 6
                colour = (0, 255, 0)
            
            cv.rectangle(image, (center_x1, center_y1), (center_x2, center_y2), colour, 1)
        
        else:
            colour = (0,0,255)
            cv.rectangle(image, (center_x1, center_y1), (center_x2, center_y2), colour, 1)
            
            #voice command = "Go right"
            if pupil_x < center_x1:
                self.shared_variable.value = 1
            
            #voice command = "Go left"
            elif pupil_x > center_x2:
                self.shared_variable.value = 0
                
            #voice command = "Go up" 
            elif pupil_y > center_y1:
                self.shared_variable.value = 2
            
            #voice command = "Go down"
            elif pupil_y < center_y2:
                self.shared_variable.value = 3  

        #Place the text on frame
        cv.putText(image, voice_commands[self.shared_variable.value], (200, 100), cv.FONT_HERSHEY_SIMPLEX, 1, colour, 2, cv.LINE_AA)

    def capture(self, frame, number_of_eyes_captured):
        with self.mp_face_mesh.FaceMesh(
            max_num_faces = 1,
            refine_landmarks = True,
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5
        ) as face_mesh:

            
            # ret, frame = self.cap.read()
            # if not ret:
            #     print("Not ret")
                

            #Flipping the frame
            # image = cv.flip(frame, 0)
            image = cv.flip(frame, 1)
            self.frame_original = image.copy()
            image, results = self.mediapipe_detection(image, face_mesh)
            pupils_coords = None
            if results.multi_face_landmarks:
                for _, facial_landmarks in enumerate(results.multi_face_landmarks):
                    #Detect coordinates of each part 
                    left_eye_coords = self.part_detection(self.LEFT_EYE, facial_landmarks, image.shape)
                    right_eye_coords = self.part_detection(self.RIGHT_EYE, facial_landmarks, image.shape)
                    left_iris_coords = self.part_detection(self.LEFT_IRIS, facial_landmarks, image.shape)
                    right_iris_coords = self.part_detection(self.RIGHT_IRIS, facial_landmarks, image.shape)
                    pupils_coords = self.part_detection(self.CENTERS, facial_landmarks, image.shape)

                    #Display each part on the frame
                    self.display_part(image, left_eye_coords, (0,255,255), False)
                    self.display_part(image, right_eye_coords, (0,255,255), False)
                    self.display_part(image, left_iris_coords, (0,255,255), True)
                    self.display_part(image, right_iris_coords, (0,255,255), True)
                    self.display_part(image, pupils_coords, (0,255,255), True, True)
            if pupils_coords:
                self.get_distance(pupils_coords[0], pupils_coords[1])


                self.correct_position(image, pupils_coords, left_iris_coords, right_iris_coords, number_of_eyes_captured)

            if self.shared_variable.value == 6:
                self.is_eye_in_square = True
            else:
                self.is_eye_in_square = False
            
            return image





