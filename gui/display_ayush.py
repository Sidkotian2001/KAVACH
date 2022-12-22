from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.colorpicker import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from iris_local_kivy import iris_voice
from models.detect import Checkup
import os
from pdf import create_pdf
import subprocess

Window.size = (640, 480)
Window.clearcolor = (1,1,1,1)


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

# class to accept user info and validate it
class loginWindow(Screen):
	email = ObjectProperty(None)
	pwd = ObjectProperty(None)


	def validate(self):

		## reading all the data stored
		## if login.csv does not exist then create it
		# try:
		# 	users=pd.read_csv('login.csv')
		# except:
		# 	users=pd.DataFrame(columns=['Name','Email','Password'])
		# 	users.to_csv('login.csv',index=False)

		# # validating if the email already exists
		# if self.email.text not in users['Email'].unique():
		# 	popFun()
		# else:
		# 	# validating if the password is correct
		# 	user_email = users[users['Email'] == self.email.text]
		# 	if user_email['Password'].values[0] == self.pwd.text:
		# 		# switching the current screen to display validation result
		# 		sm.current = 'logdata'

		# 		# reset TextInput widget
		# 		self.email.text = ""
		# 		self.pwd.text = ""
		# 	else:

		# 		popFun()
		sm.current = 'logdata'
			


# class to accept sign up info
class signupWindow(Screen):
	name2 = ObjectProperty(None)
	email = ObjectProperty(None)
	pwd = ObjectProperty(None)
	def signupbtn(self):
		# reading all the data stored
		#if login.csv does not exist then create it
		try:
			users=pd.read_csv('login.csv')
		except:
			users=pd.DataFrame(columns=['Name','Email','Password'])
			users.to_csv('login.csv',index=False)
		# creating a DataFrame of the info
		user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
							columns = ['Name', 'Email', 'Password'])
		if self.email.text != "":
			if self.email.text not in users['Email'].unique():

				# if email does not exist already then append to the csv file
				# change current screen to log in the user now
				user.to_csv('login.csv', mode = 'a', header = False, index = False)
				sm.current = 'login'
				self.name2.text = ""
				self.email.text = ""
				self.pwd.text = ""
		else:
			# if values are empty or invalid show pop up
			popFun()
	
# class to display validation result
class logDataWindow(Screen):
	dr = ObjectProperty(None)
	amd = ObjectProperty(None)
	cataract = ObjectProperty(None)
	glaucoma = ObjectProperty(None)

	def runbtn(self):
		global obj, categories
		obj = Checkup("../images/2_cataract/cataract_004.png")

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

		sm.current = 'display_patient_details'

# class for managing screens
class WindowManager(ScreenManager):
	pass

counter = 0

class VideoCapture(Screen):
	def __init__(self, **kwargs):
		super(VideoCapture, self).__init__(**kwargs)
		
		self.texture = None
		self.iris_obj = None
		self.number_of_eyes_captured = 0
		self.is_eye_in_square = False
		self.frame_original = None

		#create a Label widget
		self.label = Label(text = "Image Capture",
						font_size = 30,
						color = (0,0,0,1),
						size_hint = (0.5, 0.1),
						pos_hint = {'center_x' : .5, 'center_y': .9}
						)
		self.background = Image(source = 'wp_3.jpg',
						allow_stretch = True,
						keep_ratio = False
						)
		self.img1 = Image(size_hint = (.96, .72),
                        pos_hint = {'center_x' : .5, 'center_y': .60}
                        )
        
        #Button 0
		self.button0 = Button(text = "Start video",
                        size_hint = (0.15, 0.1),
                        pos_hint = {'center_x' : .25, 'center_y': .15},
						background_normal = '',
    					background_color = (0.50, 0.50,0.80, 1),
                        disabled = False,
						on_release = self.start_video
                        )

        #Button 1
		self.button1 = Button(text = "Capture",
					size_hint = (0.15, 0.1),
					pos_hint = {'center_x' : .50, 'center_y': .15},
					background_normal = '',
    				background_color = (0.50, 0.50,0.80, 1),
					disabled = True,
					on_release = self.save_img
					)

		#Button 2
		self.button2 = Button(text = "View Image",
					size_hint = (0.15, 0.1),
					pos_hint = {'center_x' : .75, 'center_y': .15},
					disabled = True,
					background_normal = '',
    				background_color = (0.50, 0.50,0.80, 1),
					on_release =  self.view_image
					)
		
		#Button 3
		self.button3 = Button(text = "Next",
                    size_hint = (0.15, 0.1),
                    pos_hint = {'center_x' : .75, 'center_y': .05},
                    disabled = True,
                    background_normal = '',
    				background_color = (0.50, 0.50,0.80, 1),
                    on_release = self.next_screen
                    )

		self.iris_obj = iris_voice()
		self.add_widget(self.background)
		self.add_widget(self.img1)
		self.add_widget(self.label)
		self.add_widget(self.button0)
		self.add_widget(self.button1)
		self.add_widget(self.button2)
		# self.add_widget(self.button3)
		self.clock_schedule()

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
		sm.current = 'view_images'

	def clock_schedule(self):
		Clock.schedule_interval(self.update, 1.0/33.0)

	def update(self, _):

		if self.button0.disabled == True:
			
			frame = self.iris_obj.capture(self.number_of_eyes_captured)
			self.frame_original = self.iris_obj.frame_original
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


p_n = ''
# p_e = ''
p_m = ''
p_a = ''
p_g = ''
class patientWindow(Screen):
    patient_name = ObjectProperty(None)
    # patient_email = ObjectProperty(None)
    patient_mobile = ObjectProperty(None)
    patient_age = ObjectProperty(None)
    patient_gender = ObjectProperty(None)

    def submit_info(self):
        globals()['p_n'] = self.patient_name.text
        # globals()['p_e'] = self.patient_email.text
        globals()['p_m'] = self.patient_mobile.text
        globals()['p_a'] = self.patient_age.text
        globals()['p_g'] = self.patient_gender.text
        print(globals()['p_n'])
        print(globals()['p_m'])
        
    
class DisplayPatientWindow(Screen):
	patient_name = StringProperty()
	# patient_email = StringProperty()
	patient_mobile = StringProperty()
	patient_age = StringProperty()
	patient_gender = StringProperty()


	def display_info(self):
		self.patient_name = globals()['p_n']
		# self.patient_email = globals()['p_e']
		self.patient_mobile = globals()['p_m']
		self.patient_age = globals()['p_a']
		self.patient_gender = globals()['p_g']

	def generate_pdf(self):
		categories = globals()['categories']
		
		pdf_obj = create_pdf('Medical.pdf', self.patient_name, self.patient_age,
						self.patient_mobile, self.patient_gender)
		
		pdf_obj.build_pdf(categories)
	
		# exit()

class View_Images(Screen):

	def __init__(self, **kw):
		super().__init__(**kw)
		self.c = globals()['counter']
		self.img1 = Image(source = 'camera_icon.png', 
			allow_stretch = True,
			keep_ratio = False,
			size_hint = (0.4, 0.4),
			pos_hint = {'center_x': 0.25, 'center_y' : 0.5}
			)
		
		self.img2 = Image(source = 'camera_icon.png',
			allow_stretch = True,
			keep_ratio =  False,
			size_hint =  (0.4, 0.4),
			pos_hint = {'center_x': 0.75, 'center_y': 0.5}
		)

		self.add_widget(self.img1)
		self.add_widget(self.img2)

	def show_images(self):
		self.c = globals()['counter']
		self.img1.source = 'image_taken_{}.jpg'.format(str(self.c))
		self.img2.source = 'image_taken_{}.jpg'.format(str(self.c + 1))
		globals()['counter'] += 2
	
	def previous_screen(self):
		self.img1.source = self.img2.source = 'camera_icon.png'
		sm.current = 'videofeed'


# kv file
kv = Builder.load_file('login.kv')
sm = WindowManager()


# class that builds gui
class loginMain(App):
	def build(self):
		# adding screens

		sm.add_widget(loginWindow(name='login'))
		sm.add_widget(signupWindow(name='signup'))
		sm.add_widget(logDataWindow(name='logdata'))
		sm.add_widget(VideoCapture(name='videofeed'))
		sm.add_widget(View_Images(name = 'view_images'))
		sm.add_widget(patientWindow(name='patient_details'))
		sm.add_widget(DisplayPatientWindow(name = 'display_patient_details'))
		return sm

# driver function
if __name__=="__main__":
	loginMain().run()