from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.properties import ObjectProperty
from kivy.graphics import Ellipse, RoundedRectangle, Rectangle, Color
from kivy.config import Config

from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from iris_local_kivy import iris_voice

Config.set('graphics', 'resizable', False)

Window.size = (940, 600)
# Window.clearcolor = (0,0.267,0.4,1)
Window.clearcolor = (0,0,0,1)

class WindowManager(ScreenManager):
    pass

p_fn = ''
p_ln = ''
p_m = ''
p_a = ''
p_g = ''



class patientWindow(Screen):
    patient_firstname = ObjectProperty(None)
    patient_lastname = ObjectProperty(None)
    patient_mobile = ObjectProperty(None)
    patient_age = ObjectProperty(None)
    patient_gender = ObjectProperty(None)

    def submit_info(self):
        globals()['p_fn'] = self.patient_firstname.text
        globals()['p_ln'] = self.patient_lastname.text
        globals()['p_m'] = self.patient_mobile.text
        globals()['p_a'] = self.patient_age.text
        globals()['p_g'] = self.patient_gender.text
        print(globals()['p_fn'])
        print(globals()['p_g'])

#Global counter varible
counter = 0

class VideoCapture(Screen):

    def __init__(self, **kwargs):
        super(VideoCapture, self).__init__(**kwargs)

        self.texture = None
        self.iris_obj = None
        self.number_of_eyes_captured = 0
        self.is_eye_in_square = False
        self.frame_original = None
        self.pos_dim = 75
        self.width_dim = 100
        self.height_dim = 200

        with self.canvas:
            Color(0,0.267,0.4,1)
            self.rect = Rectangle(pos = self.pos, size = (self.width, self.height))
            self.bind(pos = self.update_rect, size = self.update_rect)

            Color(0.5,0.5,0.5,1)
            self.round_rect = RoundedRectangle(pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 50),
                                            size = (self.width - self.width_dim, self.height - self.height_dim),
                                            radius = [20])
            self.bind(pos = self.update_round_rect, size = self.update_round_rect)

            Color(0.85,0.85,0.85,1)
            self.ellipse0 = Ellipse(pos= (200, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipse0, size = self.update_ellipse0)

            Color(0.85,0.85,0.85,1)
            self.ellipse1 = Ellipse(pos= (350, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipse1, size = self.update_ellipse1)

            Color(0.85,0.85,0.85,1)
            self.ellipse2 = Ellipse(pos= (500, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipse2, size = self.update_ellipse2)

            Color(0.85,0.85,0.85,1)
            self.ellipse3 = Ellipse(pos= (650, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipse3, size = self.update_ellipse3)




        #Infyuva tech image
        self.img0 = Image(source = 'infyuva_tech-removebg-preview.png',
                        size_hint = (0.171, 0.1),
                        pos_hint = {'center_x' : .2, 'center_y' : .840}
                        )

        #Button 0 - Start/Stop Video
        self.button0 = Button(size_hint = (0.08, 0.13),
                        pos = (207, 32),
                        background_normal = 'power_button.png',
                        background_disabled_normal = 'power_button_disabled.png',
                        disabled = False,
                        on_release = self.start_video
        )

        #Button 1 - Capture Image
        self.button1 = Button(size_hint = (0.08, 0.09),
                        pos = (357 , 45),
                        # pos_hint = {'center_x' : .423, 'center_y': .1230},
                        background_normal = 'cam_1-removebg-preview.png',
                        background_disabled_normal = 'cam_1-removebg-preview_disabled.png',
                        disabled = True,
                        on_release = self.save_img
        )

        #Button 2 - Flash
        self.button2 = Button(size_hint = (0.08, 0.12),
                        pos = (507, 30),
                        background_normal = 'flash.png',
                        background_disabled_normal = 'flash_disabled.png',
                        disabled = True,
                        background_color = (0.50, 0.50,0.80, 1),
                        on_release =  self.view_image
        )

        #Button 3 - View Images
        self.button3 = Button(size_hint = (0.1, 0.15),
                        pos = (647, 28),
                        background_normal = 'gallery.png',
                        background_disabled_normal = 'gallery.png',
                        disabled = True,
                        background_color = (0.50, 0.50,0.80, 1),
                        on_release = self.next_screen
        )

        self.iris_obj = iris_voice()
        self.add_widget(self.img0)
        self.add_widget(self.button0)
        self.add_widget(self.button1)
        self.add_widget(self.button2)
        self.add_widget(self.button3)
        self.clock_schedule()
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_round_rect(self, *args):
        self.round_rect.pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 50)
        self.round_rect.size = (self.width - self.width_dim, self.height - self.height_dim)
        self.round_rect.radius = [20]
    
    def update_ellipse0(self, *args):
        self.ellipse0.pos = (200, 25)
        self.ellipse0.size = (90 , 90)
    
    def update_ellipse1(self, *args):
        self.ellipse1.pos = (350, 25)
        self.ellipse1.size = (90 , 90)
        
    def update_ellipse2(self, *args):
        self.ellipse2.pos = (500, 25)
        self.ellipse2.size = (90 , 90)

    def update_ellipse3(self, *args):
        self.ellipse3.pos = (650, 25)
        self.ellipse3.size = (90 , 90)

    def change_flash(self, _):
        print("This function works on the flash hardware")

    def view_image(self, _):
        self.button0.disabled = False
        del self.iris_obj
        self.iris_obj = iris_voice()
        sm.current = 'view_images'

    def next_screen(self):
        #cdestroy the camera object
        self.button0.disabled = False
        del self.iris_obj
        self.iris_obj = iris_voice()
        self.number_of_eyes_captured = 0
        # sm.current = 'view_images'

    def clock_schedule(self):
        Clock.schedule_interval(self.update, 1.0/33.0)

    def update(self, _):
        if self.button0.disabled == True:

            frame = self.iris_obj.capture(self.number_of_eyes_captured)
            self.frame_original = self.iris_obj.frame_original
            self.is_eye_in_square = self.iris_obj.is_eye_in_square
            # frame = cv2.flip(frame, 0)	


            buf = frame.tobytes()

            self.texture = Texture.create(size = (640, 480), colorfmt = 'bgr')
            #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 

            self.texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')

            self.round_rect.texture = self.texture
        else:
            pass
            # self.img1.source = 'camera_icon.png'

    def start_video(self, _):
        self.button0.disabled = True
        self.button1.disabled = False
        self.button2.disabled = False
        self.button3.disabled = False

    def save_img(self, _):
        if self.is_eye_in_square == True:
            c = globals()['counter']
            cv2.imwrite('image_taken_{}.jpg'.format(str(self.number_of_eyes_captured + c)), self.frame_original)
            self.number_of_eyes_captured += 1
        if self.number_of_eyes_captured > 1:
            self.next_screen()
        else:
            pass

    def change_illumination(self, _):
        print("This button will adjust the illumination")

class evalautionWindow(Screen):
    pass

d_fn = ''
d_ln = ''
d_m = ''
d_a = ''
d_pass = ''

class signupWindow(Screen):
    doctor_firstname = ObjectProperty(None)
    doctor_lastname = ObjectProperty(None)
    doctor_mobile = ObjectProperty(None)
    doctor_age = ObjectProperty(None)
    doctor_password = ObjectProperty(None)

    def submit_info(self):
        try:
            users = pd.read_csv('login.csv')
        except:
            users = pd.DataFrame(columns = ['First Name','Last Name', 'Mobile', 'Age', 'Password'])
            users.to_csv('login.csv', index = False)
        
        user = pd.DataFrame([[self.doctor_firstname.text, self.doctor_lastname.text,
                            self.doctor_mobile.text, self.doctor_age.text, 
                            self.doctor_password.text]])        
        if self.doctor_mobile.text != '':
            if self.doctor_mobile.text not in users['Mobile'].unique():
                user.to_csv('login.csv', mode = 'a', header = False, index = False)
                # sm.current = 'login'
                self.doctor_firstname.text = ''
                self.doctor_lastname.text = ''
                self.doctor_mobile = ''
                self.doctor_age = ''
                self.doctor_password = ''

        else:
            popFun()
    
kv = Builder.load_file('components.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        # sm.add_widget(signupWindow(name = 'signup'))
        sm.add_widget(VideoCapture(name='videofeed'))
        # sm.add_widget(patientWindow(name = 'patientinfowindow'))
        # sm.add_widget(evalautionWindow(name = 'evalautioninfoWindow'))
        return sm

if __name__ == '__main__':
    loginMain().run()