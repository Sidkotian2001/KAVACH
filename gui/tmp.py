from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '600')


# import all the relevant classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd
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
		print("running")
		os.system('python3 /home/ayush/Documents/Machine_learning/INFYUVA/final/models/detect.py')
	pass

# class for managing screens
class windowManager(ScreenManager):
	pass


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
# class that builds gui
class loginMain(App):
	def build(self):
		return sm

# driver function
if __name__=="__main__":
	loginMain().run()
