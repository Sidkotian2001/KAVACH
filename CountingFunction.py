"""Counting Function"""
# The objective of this file is to count only class=0 which is related to people 
# using the default model that comes with YOLOv8, which is yolov8n.pt
# By default, this program will use the webcam. But if you want to use a video
# please follow the steps marked as A, B and C.

import cv2
import json
from ultralytics import YOLO
import supervision as sv
import numpy as np


class Counter:
    """A) If you want to use a video please uncomment the next line and change the path of
    #the video you want to use."""

    

    def __init__(self,path):
        self.video = path
        self.Total_detections = []
        self.main()


    def main(self):
        "B) Please uncomment the next line in case you want to use a video"
        video_info = sv.VideoInfo.from_video_path(self.video)

        
        count_max=0
        count=0

        dictionary = {
            "Vehicles": count_max,
            "People": count_max
            }

        #Call the model
        #As default the webcam is going to be used (source=0)
        "C) In case a video is intended to use, please change to (source=video)"
        model = YOLO("yolov8l.pt")
        for result in model.track(source=self.video, show=True, stream=True, agnostic_nms=True):
            
            frame = result.orig_img
            detections = sv.Detections.from_yolov8(result)

            #Function to avoid the program to crash in case there is not a single detection
            if result.boxes.id is not None:
                detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)


            for r in result:
                for c in r.boxes.cls:
                    if model.names[int(c)] == 'car' or model.names[int(c)]=='motorcycle':
                        count=count+1


            count_max=max(count_max,count)
            count = 0
            # print("Hello:",detections)

            #At follows declare the class person as object to detect ,2,3,4,7,8,77]
            detections = detections[(detections.class_id == 0)]
            

            

            #Count all the people detected per frame
            Fcount = np.count_nonzero(detections.tracker_id)

            #Extract the count of all the people in each frame considering the duplicated IDs
            #therefore, If the person was detected, an ID was assigned and if it is occluded 
            #or went out of the FOV and returned back, that person will preserve the same ID
            #and the counting function won't double count that person 
            if Fcount == 0:
                if detections.tracker_id == None or detections.tracker_id =="":
                    print("None")
            else:
                count_detections = detections.tracker_id.tolist()
                for i in count_detections:
                    if i not in self.Total_detections:
                        self.Total_detections.append(i)

            Actual_detection = len(self.Total_detections)
            print('Max Vehicle Count:'+str(count_max))
            print('Total number of detected people:' + str(Actual_detection))

            dictionary["Vehicles"]=count_max
            dictionary["People"]=Actual_detection

            json_object = json.dumps(dictionary, indent=4)

            with open("count.json", "w") as outfile:
                outfile.write(json_object)

            #Format on how and what each Bounding box will contain
            labels = [
                f"{'ID:'} {tracker_id} {model.model.names[class_id]} {confidence:0.2f} {'Total:'} {Actual_detection}"
                for _, confidence, class_id, tracker_id 
                in detections
            ]



            #The things weare going to show in each Frame
            # frame = box_annotator.annotate(
            #     scene=frame, 
            #     detections=detections,
            #     labels=labels
            # )


            if cv2.waitKey(1) and ord('q')==0xFF:
                
                break 


if __name__ == "__main__":
    path="/home/sid009/KAVACH/kavach_github/output_video.mp4"
    Counter(path)

