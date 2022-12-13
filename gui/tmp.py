from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '600')


# import all the relevant classes
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from iris_local_kivy import iris_voice
import os
#class for running model
class runningWindow(Screen):
	pass
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

		# validating if the email already exists
		if self.email.text not in users['Email'].unique():
			popFun()
		else:
			# validating if the password is correct

			# switching the current screen to display validation result
			sm.current = 'logdata'

			# reset TextInput widget
			self.email.text = ""
			self.pwd.text = ""


# class to accept sign up info
class signupWindow(Screen):
	name2 = ObjectProperty(None)
	email = ObjectProperty(None)
	pwd = ObjectProperty(None)
	def signupbtn(self):

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
	def runbtn(self):
		os.system('python3 /home/ayush/Documents/Machine_learning/INFYUVA/final/models/detect.py')
	pass

# class for managing screens
class windowManager(ScreenManager):
	pass

class VideoCapture(Screen):
	def __init__(self, **kwargs):
		super(VideoCapture, self).__init__(**kwargs)
		self.texture = None
		self.iris_obj = None
		self.number_of_eyes_captured = 0
		self.is_eye_in_square = False
		self.frame_original = None
        # self.layout = FloatLayout(
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

	def save_img(self, _):
		if self.is_eye_in_square == True:
			cv2.imwrite('image_taken_{}.png'.format(str(self.number_of_eyes_captured)), self.frame_original)
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


# kv file
kv = Builder.load_file('login.kv')
sm = windowManager()

# reading all the data stored
#if login.csv does not exist then create it
try:
    users=pd.read_csv('login.csv')
except:
    users=pd.DataFrame(columns=['Name','Email','Password'])
    users.to_csv('login.csv',index=False)

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(runningWindow(name='running'))
sm.add_widget(VideoCapture(name='video'))
# class that builds gui
class loginMain(App):
	def build(self):
		return sm

# driver function
if __name__=="__main__":
	loginMain().run()
