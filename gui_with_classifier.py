#!/usr/bin/env python
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Ellipse, RoundedRectangle, Rectangle, Color
from kivy.config import Config
from kivy.clock import Clock
from kivy_garden.filebrowser import FileBrowser
import os
import cv2
from kivy.graphics.texture import Texture
import sqlite3

import os
import json
from docopt import docopt
import torch
import sense.display
from sense.controller_3 import Controller
from sense.downstream_tasks.nn_utils import LogisticRegression
from sense.downstream_tasks.nn_utils import Pipe
from sense.downstream_tasks.postprocess import PostprocessClassificationOutput
from sense.loading import build_backbone_network
from sense.loading import load_backbone_model_from_config


Window.size = (940, 600)
Window.clearcolor = (0,0.267,0.4,1)
Window.resize = False

def recordvideo(video_path, start_frame_number):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the video frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out =  cv2.VideoWriter('output_video.mp4', fourcc, 30, (frame_width, frame_height))

    current_frame_number = 0
    # Loop through the video frames
    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            
            # Add a rectangle to the frame
            cv2.rectangle(frame, (50, 50), (frame_width - 50, frame_height - 50), (0, 255, 0), 3)

            # Write the modified frame to the output video
            if current_frame_number >= start_frame_number:
                out.write(frame)

            # Display the frame
            # cv2.imshow('Frame', frame)
            current_frame_number += 1
            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # Release the video capture and writer objects, and close all windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def run_custom_classifier():


    custom_classifier = "/home/sid009/KAVACH/sense_hack_action/tools/cctvviolence/checkpoints"
    camera_id = 0
    path_in = "/home/sid009/KAVACH/sense_hack_action/tools/sense_studio/Violence_videos/Fighting/fighting5.mp4"
    path_out = None
    title = "my video"
    use_gpu = False
    display_fn = None
    title = None
    stop_event = None
    # Load backbone network according to config file
    backbone_model_config, backbone_weights = load_backbone_model_from_config(custom_classifier)

    try:
        # Load custom classifier10
        checkpoint_classifier = torch.load(os.path.join(custom_classifier, 'best_classifier.checkpoint'))
    except FileNotFoundError:
        msg = ("Error: No such file or directory: 'best_classifier.checkpoint'\n"
               "Hint: Provide path to 'custom_classifier'.\n")
        if display_fn:
            display_fn(msg)
        else:
            print(msg)
        return None

    # Create backbone network
    backbone_network = build_backbone_network(backbone_model_config, backbone_weights,
                                              weights_finetuned=checkpoint_classifier)
    # print(backbone_network)

    with open(os.path.join(custom_classifier, 'label2int.json')) as file:
        class2int = json.load(file)
    INT2LAB = {value: key for key, value in class2int.items()}

    
    

    gesture_classifier = LogisticRegression(num_in=backbone_network.feature_dim,
                                            num_out=len(INT2LAB))
    gesture_classifier.load_state_dict(checkpoint_classifier)
    gesture_classifier.eval()

    # Concatenate feature extractor and met converter
    net = Pipe(backbone_network, gesture_classifier)

    postprocessor = [
        PostprocessClassificationOutput(INT2LAB, smoothing=4)
    ]

    display_ops = [
        sense.display.DisplayFPS(expected_camera_fps=net.fps,
                                 expected_inference_fps=net.fps / net.step_size),
        sense.display.DisplayTopKClassificationOutputs(top_k=1, threshold=0.5),
        
    ]
    display_results = sense.display.DisplayResults(title=title, display_ops=display_ops, display_fn=display_fn)
    # Run live inference
    controller = Controller(
        neural_network=net,
        post_processors=postprocessor,
        results_display=display_results,
        callbacks=[],
        camera_id=camera_id,
        path_in=path_in,
        path_out=path_out,
        use_gpu=use_gpu,
        stop_event=stop_event,
    )
    # print(controller)
    # img_final = controller.run_inference()
    controller.run_inference()

    if controller.record_video == False:
        return 0
    
    return controller.frame_start

class WindowManager(ScreenManager):
    pass

class loginWindow(Screen):
    
    login_username = ObjectProperty(None)
    login_password = ObjectProperty(None)
    infyuva_label = ObjectProperty(None)
        
    def submit_login(self):
        try:
            conn = sqlite3.connect('login.db')
            c = conn.cursor()
            c.execute("SELECT * FROM login WHERE username = ? AND password = ?", (self.login_username.text, self.login_password.text))
            data = c.fetchall()
            if data:
                sm.add_widget(VideoCapture(name='videofeed'))
                sm.current = 'videofeed'
            else:
                self.login_username.text = ''
                self.login_password.text = ''
        except Exception as e:
            print(e)

class signupWindow(Screen):
    user_name = ObjectProperty(None)
    user_username = ObjectProperty(None)
    user_mobile = ObjectProperty(None)
    user_age = ObjectProperty(None)
    user_password = ObjectProperty(None)

    def submit_signup(self):
        name_flag = str(self.user_name.text).isalpha()
        age_flag = str(self.user_age.text).isnumeric()
        mobile_flag = str(self.user_mobile.text).isnumeric()

        if len(str(self.user_age.text)) < 0 or len(str(self.user_age.text)) > 3:
            age_flag = False
        if len(str(self.user_mobile.text)) != 10:
            mobile_flag = False
        if name_flag and age_flag and mobile_flag:
            try:
                conn = sqlite3.connect('login.db')
                c = conn.cursor()
                c.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?)", (self.user_name.text, self.user_username.text, self.user_mobile.text, self.user_age.text, self.user_password.text))
                conn.commit()
                conn.close()
                self.user_name.text = ''
                self.user_age.text=''
                self.user_username.text = ''
                self.user_mobile.text = ''
                self.user_password.text = ''
                sm.current = 'logininfoWindow'


            except:
                #make a login database
                conn = sqlite3.connect('login.db')
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS login (Name, Username, mobile, age, password)")
                conn.commit()
                #insert into the database
                c.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?)", (self.user_name.text, self.user_username.text, self.user_mobile.text, self.user_age.text, self.user_password.text))
                conn.close()
                self.user_name.text = ''
                self.user_age.text=''
                self.user_username.text = ''
                self.user_mobile.text = ''
                self.user_password.text = ''
                sm.current = 'logininfoWindow'
        else:
            if not name_flag:
                self.user_name.text = ''
            if  not age_flag:
                self.user_age.text = ''
            if not mobile_flag:
                self.user_mobile.text = ''

class VideoCapture(Screen):

    def __init__(self, **kwargs):
        super(VideoCapture, self).__init__(**kwargs)
        self.img = Image()
        self.texture = None
        self.video_path = "/home/sid009/KAVACH/sense_hack_action/tools/sense_studio/Violence_videos/Fighting/fighting5.mp4"
        
        self.pos_dim = 75
        self.width_dim = 100
        self.height_dim = 200
        
        
        with self.canvas:
            Color(0,0.267,0.4,1)
            self.rect = Rectangle(pos = self.pos, size = (self.width, self.height))
            self.bind(pos = self.update_rect, size = self.update_rect)

            Color(1,1,1,1)
            self.round_rect = RoundedRectangle(pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 50),
                                            size = (self.width - self.width_dim, self.height - self.height_dim),
                                            radius = [20])
            self.bind(pos = self.update_round_rect, size = self.update_round_rect)

        # self.add_widget(self.img)
        start_frame_number = run_custom_classifier()
        recordvideo(video_path=self.video_path, 
                            start_frame_number=start_frame_number)
        self.capture = cv2.VideoCapture("/home/sid009/KAVACH/kavach_github/output_video2.mp4")
        
        self.clock_schedule()
        # self.size_hint = (1, 9/16)
    
    
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_round_rect(self, *args):
        self.round_rect.pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 50)
        self.round_rect.size = (self.width - self.width_dim, self.height - self.height_dim)
        self.round_rect.radius = [20]

    def clock_schedule(self):
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self, _):
        # if self.button0.disabled == True:
        _, frame = self.capture.read()
        
        frame = cv2.resize(frame, (640, 480))
        # print(frame.shape)
        # frame = cv2.flip(frame, 0)
        # frame = cv2.flip(frame, 1)
        # frame = cv2.flip(frame, 0)	

        buf = frame.tobytes()

        self.texture = Texture.create(size = (640, 480), colorfmt = 'bgr')
        # self.texture = Texture.create(size = (1280, 720), colorfmt = 'bgr')

        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 

        self.texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.round_rect.texture = self.texture

kv = Builder.load_file('layout.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        sm.add_widget(loginWindow(name = 'logininfoWindow'))
        sm.add_widget(signupWindow(name = 'signupinfoWindow'))
        
        return sm

def main():
    loginMain().run()

if __name__ == "__main__":
    main()