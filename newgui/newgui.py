from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.effectwidget import AdvancedEffectBase, EffectWidget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color
from kivy.config import Config
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

class evalautionWindow(Screen):
    pass

kv = Builder.load_file('components.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        sm.add_widget(patientWindow(name = 'patientinfowindow'))
        sm.add_widget(evalautionWindow(name = 'evalautioninfoWindow'))
        return sm

if __name__ == '__main__':
    loginMain().run()