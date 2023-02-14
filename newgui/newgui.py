from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Ellipse, RoundedRectangle, Rectangle, Color
from kivy.config import Config

from kivy.clock import Clock
import os
from kivy.graphics.texture import Texture
import cv2
from iris_local_kivy import iris_voice
import pandas as pd
import sqlite3
from models.detect import Checkup


Config.set('graphics', 'resizable', False)

Window.size = (940, 600)
Window.clearcolor = (0,0.267,0.4,1)
# Window.clearcolor = (0,0,0,1)

class WindowManager(ScreenManager):
    pass



p_f = ''
p_l = ''
p_m= ''
p_a = ''
p_g = ''
class patientWindow(Screen):
    patient_firstname = ObjectProperty(None)
    patient_lastname = ObjectProperty(None)
    patient_mobile = ObjectProperty(None)
    patient_age = ObjectProperty(None)
    patient_gender = ObjectProperty(None)

    def submit_info(self):
        globals()['p_f'] = self.patient_firstname.text
        globals()['p_l'] = self.patient_lastname.text
        globals()['p_m'] = self.patient_mobile.text
        globals()['p_a'] = self.patient_age.text
        globals()['p_g'] = self.patient_gender.text


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

            Color(1,1,1,1)
            self.round_rect = RoundedRectangle(pos = (self.center_x - ((self.width - self.width_dim) / 2), self.center_y - ((self.height - self.height_dim) / 2) + 50),
                                            size = (self.width - self.width_dim, self.height - self.height_dim),
                                            radius = [20])
            self.bind(pos = self.update_round_rect, size = self.update_round_rect)

            Color(1,1,1,1)
            self.ellipse0 = Ellipse(pos= (200, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipses, size = self.update_ellipses)

            Color(1,1,1,1)
            self.ellipse1 = Ellipse(pos= (350, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipses, size = self.update_ellipses)

            Color(1,1,1,1)
            self.ellipse2 = Ellipse(pos= (500, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipses, size = self.update_ellipses)

            Color(1,1,1,1)
            self.ellipse3 = Ellipse(pos= (650, 25),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipses, size = self.update_ellipses)

        #Infyuva tech image
        self.img0 = Image(source = 'infyuva_tech-removebg-preview.png',
                        size_hint = (0.171, 0.1),
                        pos_hint = {'center_x' : .16, 'center_y' : .840}
                        )

        #Button 0 - Start/Stop Video
        self.button0 = Button(size_hint = (0.08, 0.13),
                        pos = (207, 32),
                        background_normal = 'power_button.png',
                        background_disabled_normal = 'power_button.png',
                        disabled = False,
                        on_release = self.start_video
        )

        #Button 1 - Capture Image
        self.button1 = Button(size_hint = (0.075, 0.09),
                        pos = (359 , 45),
                        # pos_hint = {'center_x' : .423, 'center_y': .1230},
                        background_normal = 'camera.png',
                        background_disabled_normal = 'camera_disabled.png',
                        disabled = True,
                        on_release = self.save_img
        )

        #Button 2 - Flash
        self.button2 = Button(size_hint = (0.08, 0.12),
                        pos = (508, 32),
                        background_normal = 'flash.png',
                        background_disabled_normal = 'flash_disabled.png',
                        disabled = True,
                        background_color = (0.50, 0.50,0.80, 1),
                        on_release =  self.view_image
        )

        #Button 3 - View Images
        self.button3 = Button(size_hint = (0.1, 0.15),
                        pos = (648, 26),
                        background_normal = 'gallery.png',
                        background_disabled_normal = 'gallery_disabled.png',
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
    
    def update_ellipses(self, *args):
        self.ellipse0.pos = (200, 25)
        self.ellipse0.size = (90 , 90)
        self.ellipse1.pos = (350, 25)
        self.ellipse1.size = (90 , 90)
        self.ellipse2.pos = (500, 25)
        self.ellipse2.size = (90 , 90)
        self.ellipse3.pos = (650, 25)
        self.ellipse3.size = (90 , 90)

    def change_flash(self, *args):
        print("This function works on the flash hardware")

    def view_image(self, *args):
        self.button0.disabled = False
        del self.iris_obj
        self.iris_obj = iris_voice()
        sm.current = 'view_images'

    def next_screen(self, *args):
        #cdestroy the camera object
        self.button0.disabled = False
        del self.iris_obj
        self.iris_obj = iris_voice()
        self.number_of_eyes_captured = 0
        sm.current = 'viewimages'


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
            # self.round_rect.source = 'flash.png'
            pass

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

class ViewImages(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.c = globals()['counter']

        with self.canvas:
            Color(0.5,0.5,0.5,0.5)
            self.ellipse1 = Ellipse(pos= (310, 45),
                size = (90 , 90),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipses, size = self.update_ellipses)

            Color(1,1,1,1)
            self.ellipse2 = Ellipse(pos= (525 , 45),
                size = (90 , 90),
                stroke_width = 20,
                stroke = (1,0,0,1),
                angle_start = 0,
                angle_end = 360)
            self.bind(pos = self.update_ellipses, size = self.update_ellipses)

        self.img1 = Image(source = 'camera.png', 
                        opacity = 0,
                        allow_stretch = True,
                        keep_ratio = False,
                        size_hint = (0.4, 0.4),
                        pos_hint = {'center_x': 0.27, 'center_y' : 0.5}
                        )

        self.img2 = Image(source = 'camera.png',
                        opacity = 0,
                        allow_stretch = True,
                        keep_ratio =  False,
                        size_hint =  (0.4, 0.4),
                        pos_hint = {'center_x': 0.73, 'center_y': 0.5}
                        )
        
        self.display_button = Button(size_hint = (0.1, 0.15),
                                pos = (308 , 45),
                                # pos_hint = {'center_x' : .423, 'center_y': .1230},
                                background_normal = 'gallery.png',
                                background_disabled_normal = 'gallery_disabled.png',
                                on_release = self.show_images
        )  

        #Button 1 - Retake Image
        self.button2 = Button(size_hint = (0.075, 0.09),
                        pos = (535 , 63),
                        # pos_hint = {'center_x' : .423, 'center_y': .1230},
                        background_normal = 'camera.png',
                        background_disabled_normal = 'camera_disabled.png',
                        disabled = False,
                        on_release = self.retake_images
        )

        
        self.next_screen_button = Button(size_hint = (0.1,0.075),
                        pos = (850, 550),
                        background_normal = 'arrow.png',
                        background_disabled_normal = 'arrow.png',
                        on_release = self.next_screen        
        )
             
			

        self.add_widget(self.img1)
        self.add_widget(self.img2)
        self.add_widget(self.next_screen_button)
        self.add_widget(self.button2)
        self.add_widget(self.display_button)
    
    def update_ellipses(self, *args):
        self.ellipse1.pos = (310, 45)
        self.ellipse1.size = (90 , 90)
        self.ellipse2.pos = (525 , 45)
        self.ellipse2.size = (90 , 90)

    def show_images(self, *args):
        self.c = globals()['counter']
        self.img1.source = 'image_taken_{}.jpg'.format(str(self.c))
        self.img2.source = 'image_taken_{}.jpg'.format(str(self.c + 1))
        self.img1.opacity = self.img2.opacity = 1
        if globals()['counter'] > 0:
            os.remove('image_taken_{}.jpg'.format(str(self.c - 1)))
            os.remove('image_taken_{}.jpg'.format(str(self.c - 2)))
        self.display_button.disabled = True
        globals()['counter'] += 2


    def retake_images(self, *args):
        self.img1.source = self.img2.source = 'camera.png'
        self.img1.opacity = self.img2.opacity = 0
        self.display_button.disabled = False
        sm.current = 'videofeed'
    
    def next_screen(self, *args):
        self.img1.source = self.img2.source = 'camera.png'
        self.img1.opacity = self.img2.opacity = 0
        self.display_button.disabled = False
        sm.current = 'evalautioninfoWindow'


p_cataract = ''
p_dr = ''
p_amd = ''
p_glaucoma = ''

class evalautionWindow(Screen):
    dr = ObjectProperty(None)
    amd = ObjectProperty(None)
    glaucoma = ObjectProperty(None)
    cataract = ObjectProperty(None)

    def run_model(self):
        global obj, categories
        obj = Checkup("../images/3_retina_disease/Retina_006.png")
        dr_flag = amd_flag = cataract_flag = glaucoma_flag = False
        if self.dr.active:
            dr_flag = True

        if self.amd.active :
            amd_flag = True

        if self.cataract.active :
            cataract_flag = True

        if self.glaucoma.active :
            glaucoma_flag = True
        obj.call_model(cataract_flag, dr_flag, amd_flag, glaucoma_flag)
        obj.show_categories()
        categories = obj.categories
        globals()['p_cataract'] = categories['cataract']
        globals()['p_dr'] = categories['dr']
        globals()['p_amd'] = categories['amd']
        globals()['p_glaucoma'] = categories['glaucoma']
        sm.current = 'reportinfoWindow'


class signupWindow(Screen):
    doctor_name = ObjectProperty(None)
    doctor_username = ObjectProperty(None)
    doctor_mobile = ObjectProperty(None)
    doctor_age = ObjectProperty(None)
    doctor_password = ObjectProperty(None)

    def submit_signup(self):
        try:
            conn = sqlite3.connect('login.db')
            c = conn.cursor()
            c.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?)", (self.doctor_name.text, self.doctor_username.text, self.doctor_mobile.text, self.doctor_age.text, self.doctor_password.text))
            conn.commit()
            conn.close()
            sm.current = 'logininfoWindow'
        except:
            #make a login database
            conn = sqlite3.connect('login.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS login (Name, Username, mobile, age, password)")
            conn.commit()
            #insert into the database
            c.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?)", (self.doctor_name.text, self.doctor_username.text, self.doctor_mobile.text, self.doctor_age.text, self.doctor_password.text))
            conn.close()
            sm.current = 'logininfoWindow'

class loginWindow(Screen):
    
    login_username = ObjectProperty(None)
    login_password = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)

        # with self.canvas:
            # Color(0.85, 0.85, 0.85, 1)
            # self.round_rect = RoundedRectangle(pos = (300, 300),
            #                                 size = (200, 50),
            #                                 radius = [10])
            # self.bind(pos = self.update_round_rect, size = self.update_round_rect)

            # Color(0.85, 0.85, 0.85, 1)
            # self.round_rect2 = RoundedRectangle(pos = (300, 300),
            #                                 size = (200, 50),
            #                                 radius = [10])
            # self.bind(pos = self.update_round_rect, size = self.update_round_rect)
        

        # self.login_username = TextInput(hint_text = 'Username',
        #     hint_text_color = (0,0,0,1),
        #     font_name = 'Inter/static/Inter-Regular.ttf',
        #     halign = 'center',
        #     background_color = (0.85,0.85,0.85,1),
        #     multiline = False,
        #     background_normal = "",
        #     background_active = "",
        #     size_hint = (0.281, 0.07),
        #     pos_hint = {'center_x' : 0.275, 'center_y' : 0.55}
        # )
            
        # self.login_password = TextInput(hint_text= 'Password',
        #     password = True,
        #     hint_text_color =  (0,0,0,1),
        #     font_name = 'Inter/static/Inter-Regular.ttf',
        #     halign = 'center',
        #     background_color = (0.85,0.85,0.85,1),
        #     multiline = False,
        #     background_normal = "",
        #     background_active = "",
        #     size_hint = (0.281, 0.07),
        #     pos_hint = {'center_x' : 0.275, 'center_y' : 0.445}

        # )

        # self.add_widget(self.login_username)
        # self.add_widget(self.login_password)
    
    def update_round_rect(self, *args):
        self.round_rect.pos = (110, 305)
        self.round_rect.size = (300, 50)
        self.round_rect2.pos = (110, 243)
        self.round_rect2.size = (300, 50)
        
    def submit_login(self):
        try:
            conn = sqlite3.connect('login.db')
            c = conn.cursor()
            c.execute("SELECT * FROM login WHERE username = ? AND password = ?", (self.login_username.text, self.login_password.text))
            data = c.fetchall()
            if data:
                sm.current = 'patientinfowindow'
            else:
                self.login_username.text = ''
                self.login_password.text = ''
                pass
        except Exception as e:
            print(e)

class ReportWindow(Screen):
    patient_name = StringProperty()
    patient_mobile = StringProperty()
    patient_age = StringProperty()
    patient_gender = StringProperty()
    cataract = StringProperty()
    dr = StringProperty()
    amd = StringProperty()
    glaucoma = StringProperty()

    def view_(self):
        self.patient_name = globals()['p_f']
        self.patient_mobile = globals()['p_m']
        self.patient_age = globals()['p_a']
        self.patient_gender = globals()['p_g']
        self.cataract = globals()['p_cataract']
        self.dr = globals()['p_dr']
        self.amd = globals()['p_amd']
        self.glaucoma = globals()['p_glaucoma']



    

        

    

        
        
    
    
kv = Builder.load_file('components.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        sm.add_widget(loginWindow(name = 'logininfoWindow'))
        sm.add_widget(signupWindow(name = 'signupinfoWindow'))
        sm.add_widget(patientWindow(name = 'patientinfowindow'))
        sm.add_widget(VideoCapture(name='videofeed'))
        sm.add_widget(ViewImages(name = 'viewimages'))
        sm.add_widget(evalautionWindow(name = 'evalautioninfoWindow'))
        sm.add_widget(ReportWindow(name = 'reportinfoWindow'))
        return sm

if __name__ == '__main__':
    loginMain().run()