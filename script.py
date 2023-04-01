import pywhatkit
import pyautogui
import keyboard as k
import time

class alerter:
    def __init__(self):
        pass

    def send_msg(self, number, location, threat_level, threat_class):

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        message = "Alert! A " + threat_level + " " + threat_class + " has been reported at " + location + " at " + current_time + ". Stay safe!"

        # Send a WhatsApp Message to the contact instantly (gives 10s to load web client before sending)
        pywhatkit.sendwhatmsg_instantly(number, message, 10)

        pyautogui.click(1335,740)
        time.sleep(4)
        k.press_and_release('enter')

def main():
    number = input("Enter phone number (including country code): ")
    location = input("Enter location: ")
    threat_level = input("Enter threat level (e.g. low, moderate, high): ")
    threat_class = input("Enter threat class (e.g. fire, tornado, earthquake): ")

    obj = alerter()
    obj.send_msg(number, location, threat_level, threat_class)

if __name__ == '__main__':
    main()
