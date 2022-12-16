# import all the relevant classes
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from functools import partial
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
import threading
import multiprocessing
import socket

#Setting window size and background color
Window.size = (640, 480)
Window.clearcolor = (1,1,1,1)

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
		os.system('../models/detect.py')
	pass

# class for managing screens
class WindowManager(ScreenManager):
	pass

class VideoCapture(Screen):
	def __init__(self, **kwargs):
		super(VideoCapture, self).__init__(**kwargs)
		
		self.shared_variable = multiprocessing.Value('i')
		# self.shared_variable.Value = 0
		self.p1 = None
		self.texture = None
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
		self.button3 = Button(text = "Next",
                    size_hint = (0.15, 0.1),
                    pos_hint = {'center_x' : .75, 'center_y': .05},
                    disabled = True,
                    #change to next screen
                    on_release = self.change_screen
                    )
		# self.button2.bind(on_press = self.change_illumination)
		self.iris_obj = iris_voice()
		self.add_widget(self.img1)
		self.add_widget(self.button0)
		self.add_widget(self.button1)
		self.add_widget(self.button2)
		# self.clock_schedule()


	def imshow(self):
		#Flag to stop the video
		self.do_vid = True

		# cv2.namedWindow('Hidden', cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
		# resize the window to (0,0) to make it invisible
		# cv2.resizeWindow('Hidden', 0, 0)
		cam = cv2.VideoCapture(0)
		

		# start processing loop
		while (self.do_vid):
			_, frame = cam.read()
			
			img = self.iris_obj.capture(frame, self.number_of_eyes_captured)
			self.frame_original = self.iris_obj.frame_original
			self.is_eye_in_square = self.iris_obj.is_eye_in_square


			# send this frame to the kivy Image Widget
			# Must use Clock.schedule_once to get this bit of code
			# to run back on the main thread (required for GUI operations)
			# the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
			Clock.schedule_once(partial(self.display_frame, img))

			cv2.imshow('Hidden', img)
			cv2.waitKey(1)
		cam.release()
		cv2.destroyAllWindows()
	
	def display_frame(self, frame, dt):
		# display the current video frame in the kivy Image widget

		# create a Texture the correct size and format for the frame
		texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

		# copy the frame data into the texture
		texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

		# flip the texture (otherwise the video is upside down
		texture.flip_vertical()

		# actually put the texture in the kivy Image widget
		self.img1.texture = texture

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
		# self.shared_variable.Value = 1
		threading.Thread(target = self.imshow, daemon = True).start()
		# self.p1 = multiprocessing.Process(target = self.imshow, args = ()).start()


	def save_img(self, _):
		# if self.is_eye_in_square == True:
		cv2.imwrite('image_taken_{}.jpg'.format(str(self.number_of_eyes_captured)), self.frame_original)
		self.number_of_eyes_captured += 1
		if self.number_of_eyes_captured > 1:
			self.do_vid = False
			# self.shared_variable.Value = 0
			# self.p1.join()
			self.send_images()
			self.next_page()
		# else:
		# 	pass

	def send_images(self):
		#Read the images
		image1 = cv2.imread('image_taken_0.jpg', 1 )
		image2 = cv2.imread('image_taken_1.jpg', 1 )

		# cv2.imshow("image1", image1)
		# cv2.imshow("Image2", image2)

		#Encode the images to a byte string
		image1_bytes = cv2.imencode('.jpg', image1)[1].tostring()
		image2_bytes = cv2.imencode('.jpg', image2)[1].tostring()

		#Set up the server socket
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind(('192.168.237.170', 5000))

		print("Started listening")
		server_socket.listen(1)
		print("Finished listening")

		#Accept a connection from the client
		client_socket, addr = server_socket.accept()

		#Send the length of the image data to the client
		client_socket.send(str(len(image1_bytes)).encode())
		#Send the entire image
		client_socket.sendall(image1_bytes)

		client_socket.send(str(len(image2_bytes)).encode())
		client_socket.sendall(image2_bytes)

		print("Sent the two images")
		client_socket.close()




	def change_illumination(self, _):
		print("This button will adjust the illumination")




class View_Images(Screen):
	pass

class GetPatientInfo(Screen):
	pass

# kv file
kv = Builder.load_file('login.kv')
sm = WindowManager()



# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(runningWindow(name='running'))
sm.add_widget(VideoCapture(name='videofeed'))
sm.add_widget(View_Images(name = 'view_images'))
# class that builds gui
class loginMain(App):
	def build(self):
		return sm

# driver function
if __name__=="__main__":
	loginMain().run()
