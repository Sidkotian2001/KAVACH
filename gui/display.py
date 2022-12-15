from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')


# import all the relevant classes
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
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
import struct
import socket
import numpy as np

#Make background color white
Window.clearcolor = (1,1,1,1)


# class for managing screens
class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)

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

		# reading all the data stored
		#if login.csv does not exist then create it
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
	def runbtn(self):
		print("running")
		os.system('python3 ../models/detect.py')
	pass



#Class for capturing the images from video feed
class VideoCapture(Screen):
	def __init__(self, **kwargs):
		super(VideoCapture, self).__init__(**kwargs)
		# Screen.__init__(self, **kwargs)

		self.MAX_DGRAM = 2**16
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(('192.168.237.170', 12348))
		self.dat = b''

		self.iris_obj = None
		self.number_of_eyes_captured = 0
		self.is_eye_in_square = False
		self.frame_original = None
		self.img1 = Image(size_hint = (.96, .72),
                        pos_hint = {'center_x' : .5, 'center_y': .60}
                        )
        
        #Button 0
		self.button0 = Button(text = "Start video",
                        size_hint = (0.15, 0.1),
                        pos_hint = {'center_x' : .25, 'center_y': .15},
                        disabled = False,
						on_release = self.start_video
                        )

        #Button 1
		self.button1 = Button(text = "Capture",
					size_hint = (0.15, 0.1),
					pos_hint = {'center_x' : .50, 'center_y': .15},
					disabled = True,
					on_release = self.save_img
					)

		#Button 2
		self.button2 = Button(text = "Flash",
					size_hint = (0.15, 0.1),
					pos_hint = {'center_x' : .75, 'center_y': .15},
					disabled = True,
					on_release = self.change_illumination
					)

		self.iris_obj = iris_voice()
		self.add_widget(self.img1)
		self.add_widget(self.button0)
		self.add_widget(self.button1)
		self.add_widget(self.button2)
		self.clock_schedule()

	def dump_buffer(self, s):
		''' Emptying buffer frame '''
		
		seg, addr = s.recvfrom(self.MAX_DGRAM)
		# print(seg[0])
		if struct.unpack('B', seg[0:1])[0] == 1:
			print('finish emptying buffer')

	def clock_schedule(self):
		Clock.schedule_interval(self.update, 0.1)

	def update(self, _):
		if self.button0.disabled == True:
			
			seg, _ = self.s.recvfrom(self.MAX_DGRAM)
			# if struct.unpack('B', seg[0:1])[0] > 1:
			# 	self.dat += seg[1:]
			# 	print("hwllo")
			# else:
			# self.dat += seg[1:]
			# print(len(seg))
			# print(len(self.dat))
			
			# if seg:
			self.dat += seg
			if len(self.dat) >= 9216000:
				img = cv2.imdecode(np.frombuffer(self.dat[:9216000], dtype = np.uint8), 1)
				# if img:
				# frame = self.iris_obj.capture(img, self.number_of_eyes_captured)
				# self.frame_original = self.iris_obj.frame_original
				# self.is_eye_in_square = self.iris_obj.is_eye_in_square
				# frame = cv2.flip(img, 0)
				# cv2.imshow("framer", frame)

				buf = img.tobytes()
			
				texture = Texture.create(size = (640, 480), 
								colorfmt = 'bgr')
				#if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
				
				texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')

				self.img1.texture = texture
				self.dat = self.dat[9216000:]
				self.dump_buffer(self.s)
			
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
		# self.manager.current = 'view_images'
		# self.root.manager.transition.direction = "right"


#Class for viewing the captured images
class View_Images(Screen):
	pass

#Class to display patient information
class GetPatientInfo(Screen):
	pass



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
		sm.add_widget(runningWindow(name='running'))
		sm.add_widget(VideoCapture(name='videofeed'))
		sm.add_widget(View_Images(name = 'view_images'))
		sm.add_widget(GetPatientInfo(name = 'patient_info'))
		return sm

# driver function
if __name__=="__main__":
	loginMain().run()
