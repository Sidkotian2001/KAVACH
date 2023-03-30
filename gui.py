from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy_garden.filebrowser import FileBrowser
import sqlite3


Window.size = (940, 600)
Window.clearcolor = (0,0.267,0.4,1)
Window.resize = False
# Window.clearcolor = (0,0,0,1)

class WindowManager(ScreenManager):
    pass

class loginWindow(Screen):
    
    login_username = ObjectProperty(None)
    login_password = ObjectProperty(None)
    infyuva_label = ObjectProperty(None)
        
    def submit_login(self):
        try:
            conn = sqlite3.connect('login.db')
            c = conn.cursor()
            c.execute("SELECT * FROM login WHERE username = ? AND password = ?", (self.login_username.text, self.login_password.text))
            data = c.fetchall()
            if data:
                self.login_username.text = ''
                self.login_password.text = ''
                print("hurray")
            else:
                self.login_username.text = ''
                self.login_password.text = ''
        except Exception as e:
            print(e)

class signupWindow(Screen):
    user_name = ObjectProperty(None)
    user_username = ObjectProperty(None)
    user_mobile = ObjectProperty(None)
    user_age = ObjectProperty(None)
    user_password = ObjectProperty(None)

    def submit_signup(self):
        name_flag = str(self.user_name.text).isalpha()
        age_flag = str(self.user_age.text).isnumeric()
        mobile_flag = str(self.user_mobile.text).isnumeric()

        if len(str(self.user_age.text)) < 0 or len(str(self.user_age.text)) > 3:
            age_flag = False
        if len(str(self.user_mobile.text)) != 10:
            mobile_flag = False
        if name_flag and age_flag and mobile_flag:
            try:
                conn = sqlite3.connect('login.db')
                c = conn.cursor()
                c.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?)", (self.user_name.text, self.user_username.text, self.user_mobile.text, self.user_age.text, self.user_password.text))
                conn.commit()
                conn.close()
                self.user_name.text = ''
                self.user_age.text=''
                self.user_username.text = ''
                self.user_mobile.text = ''
                self.user_password.text = ''
                sm.current = 'logininfoWindow'


            except:
                #make a login database
                conn = sqlite3.connect('login.db')
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS login (Name, Username, mobile, age, password)")
                conn.commit()
                #insert into the database
                c.execute("INSERT INTO login VALUES (?, ?, ?, ?, ?)", (self.user_name.text, self.user_username.text, self.user_mobile.text, self.user_age.text, self.user_password.text))
                conn.close()
                self.user_name.text = ''
                self.user_age.text=''
                self.user_username.text = ''
                self.user_mobile.text = ''
                self.user_password.text = ''
                sm.current = 'logininfoWindow'
        else:
            if not name_flag:
                self.user_name.text = ''
            if  not age_flag:
                self.user_age.text = ''
            if not mobile_flag:
                self.user_mobile.text = ''

kv = Builder.load_file('layout.kv')
sm = WindowManager()

class loginMain(App):
    def build(self):
        sm.add_widget(loginWindow(name = 'logininfoWindow'))
        sm.add_widget(signupWindow(name = 'signupinfoWindow'))
        return sm

if __name__ == '__main__':
    loginMain().run()