from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color

Window.size = (755, 480)
Window.clearcolor = (0,0.267,0.4,1)

class WindowManager(ScreenManager):
    pass

class patientWindow(Screen):
    pass

kv = Builder.load_file('components.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        sm.add_widget(patientWindow(name = 'patientinfowindow'))
        return sm

if __name__ == '__main__':
    loginMain().run()