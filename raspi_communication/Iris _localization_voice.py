import numpy as np
import cv2 as cv
import mediapipe as mp
import math
from playsound import playsound
import time
import multiprocessing


mp_face_mesh = mp.solutions.face_mesh
distances = []
focii = []
message = None
colour = None

#Landmark numbers for each part of the eyes
LEFT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
RIGHT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LEFT_IRIS = [469, 470, 471, 472]
RIGHT_IRIS = [474, 475, 476, 477]
CENTERS = [468, 473]

def mediapipe_detection(image, face):
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

def get_distance(coord1, coord2):
    
    dist_btwn_irises_in_pixels = math.dist(coord1, coord2)
    dist_btwn_irises_in_cm = 7
    face_dist_in_cm = 80
    avg_focal_length = 610
    
    focal_length = (dist_btwn_irises_in_pixels * face_dist_in_cm) / dist_btwn_irises_in_cm
    focii.append(focal_length)
    
    
    actual_distance = (avg_focal_length * dist_btwn_irises_in_cm) / dist_btwn_irises_in_pixels
    distances.append(actual_distance)

def part_detection(part, facial_landmarks, image_shape):
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


def display_part(image, coords, color, show_landmarks = False, pupils_coords = False):
    points = np.zeros(shape = (len(coords), 2))
    for idx, landmark_px in coords.items():
        points[idx] = landmark_px
        if show_landmarks == True:
            cv.circle(image, landmark_px, 1, (255, 0, 0), 2)
    points = points.astype(np.int32)
    
    #Only for center coordinates
    if pupils_coords == False:
        cv.polylines(image, [points], True, color, 2)

def create_coordinates_array(x1, y1, x2, y2):
    arr = []
    for i in range(x1, x2):
        for j in range(y1, y2):
            arr.append((i,j))
    return arr

#Displaying the horizontal and vertical axes
def display_axes(image):
    cv.line(image, (0, 240), (640, 240), (255,0,255), 1)
    cv.line(image, (320, 0), (320, 480), (255,0,255), 1)
    

#Play the voice command at particular intervals
def play_sound(shared_variable, shared_eye_count):
    msgs = ['Go left', 'Go right', 'Go up', 'Go down', 'Stay in Square', 'Get closer']
    current_time = 0
    init_time = time.time()
    while shared_variable.value != -1:
        
        current_time = time.time()
        if current_time - init_time > 3:
            print("sound:", msgs[shared_variable.value])
            playsound("Voice_commands/{}.mp3".format(msgs[shared_variable.value]))
            init_time = time.time()
            
            while (shared_variable.value == 6):
                current_time_2 = time.time()

                #Keep the eye fixed for 5 seconds
                if current_time_2 - init_time > 5:
                    if shared_eye_count[0] == 0:
                        print("Finished localizing eye 1")
                        shared_eye_count[0] = 1
                    elif shared_eye_count[1] == 0:
                        shared_eye_count[1] = 1
                    else:
                        print("Exiting the motor commands")
                        exit()
                    init_time = time.time()
    print("motor commands continuing")


def correct_position(image, pupils_coords, left_iris_coords, right_iris_coords, shared_variable, shared_eye_count):
    
    #Voice commands
    voice_commands = ['Go left', 'Go right', 'Go up', 'Go down', 'Get closer', 'Go Farther', 'Stay in Square']
    
    #Getting the distances
    upper_dist = 50
    lower_dist = 10
    actual_dist = distances[-1]

    if shared_eye_count[0] == 0:
        #Left pupil coordinates
        pupil_x = pupils_coords[0][0]
        pupil_y = pupils_coords[0][1]

        #Left iris coordinates
        iris_right = left_iris_coords[0]
        iris_top = left_iris_coords[1]
        iris_left = left_iris_coords[2]
        iris_bottom = left_iris_coords[3]

    elif shared_eye_count[1] == 0:
        #Right pupil right coordinates
        pupil_x = pupils_coords[1][0]
        pupil_y = pupils_coords[1][1]

        #Right iris coordinates
        iris_right = right_iris_coords[0]
        iris_top = right_iris_coords[1]
        iris_left = right_iris_coords[2]
        iris_bottom = right_iris_coords[3]   
    
    elif shared_eye_count[0] == 1 and shared_eye_count[1] == 1:
        #Both the eyes are localized exiting
        print("correct position : Both the eyes are localized, finished image capture")
        cv.putText(image, "correct_position : both the eyes are localized, finished image capture", (200, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
        shared_variable.value = 7
        return
    
    #Center rectangle coordinates
    center_x1, center_y1 = 300, 210
    center_x2, center_y2 = 340, 270

    arr = create_coordinates_array(center_x1, center_y1, center_x2, center_y2)
    
    #Check if eyes are in rectangles
    if  (iris_right in arr) and (iris_left in arr) and (iris_top in arr) and (iris_bottom in arr):
        #voice command = "Go Farther"
        if actual_dist > upper_dist:
            shared_variable.value = 4
            colour = (0, 0, 255)
        
        #voice command = "Get Closer"
        elif actual_dist < lower_dist:
            shared_variable.value = 5
            colour = (0, 255, 0)
        
        #voice command = "Stay in Square"
        else:
            shared_variable.value = 6
            colour = (0, 255, 0)
        
        cv.rectangle(image, (center_x1, center_y1), (center_x2, center_y2), colour, 1)
    
    else:
        colour = (0,0,255)
        cv.rectangle(image, (center_x1, center_y1), (center_x2, center_y2), colour, 1)
        
        #voice command = "Go right"
        if pupil_x < center_x1:
            shared_variable.value = 1
          
        #voice command = "Go left"
        elif pupil_x > center_x2:
            shared_variable.value = 0
            
        #voice command = "Go up" 
        elif pupil_y > center_y1:
            shared_variable.value = 2
        
        #voice command = "Go down"
        elif pupil_y < center_y2:
            shared_variable.value = 3  

    #Place the text on frame
    cv.putText(image, voice_commands[shared_variable.value], (200, 100), cv.FONT_HERSHEY_SIMPLEX, 1, colour, 2, cv.LINE_AA)


def capture(cap, shared_variable, shared_eye_count):
    message = None
    initial_time = time.time()
    with mp_face_mesh.FaceMesh(
        max_num_faces = 1,
        refine_landmarks = True,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5
    ) as face_mesh:
        while True:
            ret, frame = cap.read()
            current_time = time.time()
            if not ret:
                print("Not ret")
                break

            #Flipping the frame
            image = cv.flip(frame, 1)
            
            image, results = mediapipe_detection(image, face_mesh)
            img_height, img_width, _ = image.shape

            if results.multi_face_landmarks:
                for num, facial_landmarks in enumerate(results.multi_face_landmarks):
                    
                    #Detect coordinates of each part 
                    left_eye_coords = part_detection(LEFT_EYE, facial_landmarks, image.shape)
                    right_eye_coords = part_detection(RIGHT_EYE, facial_landmarks, image.shape)
                    left_iris_coords = part_detection(LEFT_IRIS, facial_landmarks, image.shape)
                    right_iris_coords = part_detection(RIGHT_IRIS, facial_landmarks, image.shape)
                    pupils_coords = part_detection(CENTERS, facial_landmarks, image.shape)

                    #Display each part on the frame
                    # display_part(image, left_eye_coords, (0,255,255), False)
                    # display_part(image, right_eye_coords, (0,255,255), False)
                    display_part(image, left_iris_coords, (0,255,255), True)
                    display_part(image, right_iris_coords, (0,255,255), True)
                    # display_part(image, pupils_coords, (0,255,255), True, True)
            
            display_axes(image)
            get_distance(pupils_coords[0], pupils_coords[1])


            correct_position(image, pupils_coords, left_iris_coords, right_iris_coords, shared_variable, shared_eye_count)

            cv.imshow("video feed", image)
            if cv.waitKey(5) & 0xff == ord('q') or shared_variable.value > 6:
                shared_variable.value = -1
                break
    
    #Printing the distance of user from web camera
    print(sum(distances) / len(distances))
    print(distances[-1])
    
    #Release the camera
    cap.release()
    cv.destroyAllWindows()


def main():
    cap = cv.VideoCapture(0)
    
    shared_variable = multiprocessing.Value('i')
    shared_eye_count = multiprocessing.Array('i', 2)
    shared_eye_count[0] = 0
    shared_eye_count[1] = 0

    p1 = multiprocessing.Process(target = capture, args = (cap, shared_variable, shared_eye_count))
    p2 = multiprocessing.Process(target = play_sound, args = (shared_variable, shared_eye_count))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    print("finsihed session")

if __name__ == '__main__':
    main()




