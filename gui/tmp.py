# base Class of your App inherits from the App class. 
# app:always refers to the instance of your application 
from kivy.app import App 
    
# BoxLayout arranges children in a vertical or horizontal box.
# or help to put the childrens at the desired location.
from kivy.uix.boxlayout import BoxLayout
  
###############################################
  
# creating the root widget used in .kv file
class KVBL(BoxLayout):
    '''
        no need to do anything here as
        we are building things in .kv file
    '''
    pass
  
#################################################  
# class in which name .kv file must be named KVBoxLayout.kv. 
class login(App):  
        
    def build(self):
        # returning the instance of KVBL class
        return KVBL()
  
##################################################
  
# creating the object root for BoxLayoutApp() class  
root = login() 
    
# run function runs the whole program 
# i.e run() method which calls the 
# target function passed to the constructor. 
root.run() 