from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.properties import ObjectProperty
from kivy.graphics import Ellipse, RoundedRectangle, Rectangle, Color
from kivy.config import Config

from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from iris_local_kivy import iris_voice
import pandas as pd

Config.set('graphics', 'resizable', False)

Window.size = (940, 600)
Window.clearcolor = (0,0.267,0.4,1)


# class to call the popup function
class PopupWindow(Widget):
	def btn(self):
		popFun()

# class to build GUI for a popup window
class P(FloatLayout):		
	pass

# function that displays the content
def popFun():
	show = P()
	window = Popup(title = "popup", content = show,
				size_hint = (None, None), size = (300, 300))
	window.open()

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

    pass

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
        self.width_dim = 200
        self.height_dim = 199

        with self.canvas:
            Color(0,0.267,0.4,1)
            self.rect = Rectangle(pos = self.pos, size = (self.width, self.height))
            self.bind(pos = self.update_rect, size = self.update_rect)

            Color(0.85,0.85,0.85,1)
            self.round_rect = RoundedRectangle(pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 55),
                                            size = (self.width - self.width_dim, self.height - self.height_dim),
                                            radius = [20])
            self.bind(pos = self.update_round_rect, size = self.update_round_rect)

            Color(0.85,0.85,0.85,1)
            self.ellipse0 = Ellipse(pos= (200, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_all_ellipsess, size = self.update_all_ellipsess)

            self.ellipse1 = Ellipse(pos= (350, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_all_ellipsess, size = self.update_all_ellipsess)

            self.ellipse2 = Ellipse(pos= (500, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_all_ellipsess, size = self.update_all_ellipsess)

            self.ellipse3 = Ellipse(pos= (650, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_all_ellipsess, size = self.update_all_ellipsess)




        #Infyuva tech image
        self.img0 = Image(source = 'infyuva_tech-removebg-preview.png',
                        size_hint = (0.171, 0.1),
                        pos_hint = {'center_x' : .2, 'center_y' : .840}
                        )

        #Button 0 - Start/Stop Video
        self.button0 = Button(size_hint = (0.07, 0.12),
                        pos = (212, 35),
                        background_normal = 'power_button.png',
                        background_disabled_normal = 'power_button_disabled.png',
                        disabled = False,
                        on_release = self.start_video
        )

        #Button 1 - Capture Image
        self.button1 = Button(size_hint = (0.07, 0.09),
                        pos = (362 , 45),
                        # pos_hint = {'center_x' : .423, 'center_y': .1230},
                        background_normal = 'cam_1-removebg-preview.png',
                        background_disabled_normal = 'cam_1-removebg-preview_disabled.png',
                        disabled = True,
                        on_release = self.capture_img
        )

        #Button 2 - Flash
        self.button2 = Button(size_hint = (0.07, 0.12),
                        pos = (512, 30),
                        background_normal = 'flash.png',
                        background_disabled_normal = 'flash_disabled.png',
                        disabled = True,
                        on_release =  self.change_flash
        )

        #Button 3 - View Images
        self.button3 = Button(size_hint = (0.1, 0.15),
                        pos = (647, 28),
                        background_normal = 'gallery.png',
                        background_disabled_normal = 'gallery_disabled.png',
                        disabled = True,
                        on_release = self.view_image
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
        self.round_rect.pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 30)
        self.round_rect.size = (self.width - self.width_dim, self.height - self.height_dim)
        self.round_rect.radius = [20]
    
    def update_all_ellipsess(self, *args):
        self.ellipse0.pos = (200, 25)
        self.ellipse0.size = (90 , 90)
        self.ellipse1.pos = (350, 25)
        self.ellipse1.size = (90 , 90)
        self.ellipse2.pos = (500, 25)
        self.ellipse2.size = (90 , 90)
        self.ellipse3.pos = (650, 25)
        self.ellipse3.size = (90 , 90)

    # def update_ellipse0(self, *args):
    #     self.ellipse0.pos = (200, 25)
    #     self.ellipse0.size = (90 , 90)
    
    # def update_ellipse1(self, *args):
    #     self.ellipse1.pos = (350, 25)
    #     self.ellipse1.size = (90 , 90)
        
    # def update_ellipse2(self, *args):
    #     self.ellipse2.pos = (500, 25)
    #     self.ellipse2.size = (90 , 90)

    # def update_ellipse3(self, *args):
    #     self.ellipse3.pos = (650, 25)
    #     self.ellipse3.size = (90 , 90)

    def start_video(self, _):
        self.button0.disabled = True
        self.button1.disabled = False
        self.button2.disabled = False
        self.button3.disabled = False
        
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
            frame = cv2.flip(frame, 0)

            buf = frame.tobytes()
            self.texture = Texture.create(size = (640, 480), colorfmt = 'bgr')
            self.texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')
            self.round_rect.texture = self.texture


    def capture_img(self, _):
        if self.is_eye_in_square == True:
            c = globals()['counter']
            cv2.imwrite('image_taken_{}.jpg'.format(str(self.number_of_eyes_captured + c)), self.frame_original)
            self.number_of_eyes_captured += 1
        if self.number_of_eyes_captured > 1:
            self.next_screen()

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
    doctor_username = ObjectProperty(None)
    doctor_mobile = ObjectProperty(None)
    doctor_email = ObjectProperty(None)
    # doctor_age = ObjectProperty(None)
    doctor_password = ObjectProperty(None)

    def submit_info(self):
        try:
            users = pd.read_csv('login.csv')
        except:
            users = pd.DataFrame(columns = ['First Name','Last Name', 'Mobile', 'Email', 'Username','Password'])
            users.to_csv('login.csv', index = False)
        
        user = pd.DataFrame([[self.doctor_firstname.text, self.doctor_lastname.text,
                            self.doctor_mobile.text, self.doctor_email.text, 
                            self.doctor_username.text, self.doctor_password.text]])        
        if self.doctor_mobile.text != '':
            if self.doctor_mobile.text not in users['Mobile'].unique():
                user.to_csv('login.csv', mode = 'a', header = False, index = False)
                # sm.current = 'login'
                self.doctor_firstname.text = ''
                self.doctor_lastname.text = ''
                self.doctor_mobile.text = ''
                self.doctor_email.text = ''
                self.doctor_username.text = ''
                self.doctor_password.text = ''

        else:
            popFun()
    pass

class ReportWindow(Screen):
    pass

class loginWindow(Screen):
    login_username = ObjectProperty(None)
    login_password = ObjectProperty(None)

    def validate(self):
        #Reading all the data stored
        try:
            users = pd.read_csv('login.csv')
        except:
            users = pd.DataFrame(columns = ['First Name','Last Name', 'Mobile', 'Email', 'Username', 'Password'])
            users.to_csv('login.csv', index = False)
        
        if self.login_username.text not in users['Username'].unique():
            popFun()
        
        else:
            username = users[users['Username'] == self.login_username.text]
            if username['Password'].values[0] == self.login_password.text:
                sm.current = 'videofeed'

                self.login_username.text = ''
                self.login_password.text = ''
            
            else:
                popFun()
    pass

kv = Builder.load_file('components.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        sm.add_widget(VideoCapture(name = 'videofeed'))
        sm.add_widget(loginWindow(name = 'logininfoWindow'))
        sm.add_widget(signupWindow(name = 'signup'))
        sm.add_widget(patientWindow(name = 'patientinfowindow'))
        sm.add_widget(evalautionWindow(name = 'evalautioninfoWindow'))
        sm.add_widget(ReportWindow(name = 'reportinfoWindow'))
        return sm

if __name__ == '__main__':
    loginMain().run()