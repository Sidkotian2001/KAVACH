from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from iris_local_kivy import iris_voice
import multiprocessing
import time
#Do the one button disable and enable part
Window.clearcolor = (1,1,1,1)
Window.size = (960, 720)

class VideoCapture(FloatLayout):
    def __init__(self, **kwargs):
        super(VideoCapture, self).__init__(**kwargs)
        self.texture = None
        self.iris_obj = None
        self.number_of_eyes_captured = 0
        self.is_eye_in_square = False

        # self.layout = FloatLayout()

        self.img1 = Image(size_hint = (.96, .72),
                        pos_hint = {'center_x' : .5, 'center_y': .60}
                        )
        
        #Button 0
        self.button0 = Button(text = "Start video",
                        size_hint = (0.15, 0.1),
                        pos_hint = {'center_x' : .25, 'center_y': .15},
                        disabled = False
                        )
        self.button0.bind(on_press = self.start_video)

        #Button 1
        self.button1 = Button(text = "Capture",
                        size_hint = (0.15, 0.1),
                        pos_hint = {'center_x' : .50, 'center_y': .15},
                        disabled = True
                        )
        self.button1.bind(on_press = self.save_img)

        #Button 2
        self.button2 = Button(text = "Flash",
                        size_hint = (0.15, 0.1),
                        pos_hint = {'center_x' : .75, 'center_y': .15},
                        disabled = True
                        )
        # self.button2.bind(on_press = self.change_illumination)
        self.iris_obj = iris_voice()
        self.add_widget(self.img1)
        self.add_widget(self.button0)
        self.add_widget(self.button1)
        self.add_widget(self.button2)
        self.clock_schedule()

        # p1 = multiprocessing.Process(target = self.clock_schedule)
        # p2 = multiprocessing.Process(target = self.print_shit)

        # p1.start()
        # p2.start()

        # p1.join()
        # p2.join()

    def clock_schedule(self):
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self, _):
        if self.button0.disabled == True:
                
            frame = self.iris_obj.capture(self.number_of_eyes_captured)
            self.is_eye_in_square = self.iris_obj.is_eye_in_square
            frame = cv2.flip(frame, 0)

            buf = frame.tobytes()
            
            self.texture = Texture.create(size = (640, 480), 
                            colorfmt = 'bgr')
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
            
            self.texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')

            self.img1.texture = self.texture

            
        else:
            self.img1.source = 'camera_icon.png'
    
    def start_video(self, _):
        self.button0.disabled = True
        self.button1.disabled = False
        self.button2.disabled = False
    
    def save_img(self, _):
        if self.is_eye_in_square == True:
            self.texture.save('image_taken' + str(self.number_of_eyes_captured) + '.png')
            self.number_of_eyes_captured += 1
            if self.number_of_eyes_captured > 1:
                self.next_page()
        else:
            pass
    
    def change_illumination(self, _):
        print("This button will adjust the illumination")
    
    def next_page(self):
        self.button0.disabled = True
        self.button1.disabled = True
        self.button2.disabled = True

    def print_shit(self):
        # time.sleep(0.5)
        print(self.number_of_eyes_captured)


class BaseClassApp(App):

    def build(self):
        
        obj = VideoCapture()
        return obj

if __name__ == '__main__':
    BaseClassApp().run()
