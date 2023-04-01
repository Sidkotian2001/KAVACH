import pywhatkit
import pyautogui
import keyboard as k
import time
# pywhatkit.sendwhatmsg("+91 96196 16979",
#                       "whatsapp api!",
#                       21, 10,10)

for i in range(100):
    pywhatkit.sendwhatmsg_instantly("+91 96196 16979", "Test msg.", 10, tab_close=True)

# pywhatkit.sendwhatmsg_to_group_instantly("Pika boo", "Hey Guys Again!")

# send instant message
pyautogui.click(1335, 740)
time.sleep(4)
k.press_and_release('enter')