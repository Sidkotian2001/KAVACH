import pywhatkit
import pyautogui
import keyboard as k
import time
import requests
import json
import pandas as pd

class alerter:
    def __init__(self):
        pass

    def get_ph(self, location):

        # create the API request URL
        url = "https://nominatim.openstreetmap.org/search?q={0}&format=json&limit=1".format(location)

        # send the API request
        response = requests.get(url)

        # parse the JSON response
        data = json.loads(response.text)

        # extract the latitude and longitude of the location
        lat = data[0]["lat"]
        lon = data[0]["lon"]

        # create the API request URL to search for police stations near the location
        urlp = "https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=police](around:500,{0},{1});out;".format(lat, lon)
        urlh = "https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=hospital](around:500,{0},{1});out;".format(lat, lon)

        # send the API request
        responsep = requests.get(urlp)
        responseh = requests.get(urlh)

        # parse the JSON response
        datap = json.loads(responsep.text)
        datah = json.loads(responseh.text)

        # extract the nearest police + hospitals's name and address
        pname = datap["elements"][0]["tags"]["name"]
        hname = datah["elements"][0]["tags"]["name"]

        data = [['Manipal Police Station', +919820218571], ['Chennai Central RPF', +919136339052], ['Kasba Peth Police Chowki', +918420856104]]
        police = pd.DataFrame(data, columns=['Location', 'Number']) 

        number = police.loc[police['Location'] == pname].Number
        pnum = number[0]
        return pnum, hname

    
    def send_msg(self, location, threat_level, threat_class):

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        number, hospital = self.get_ph(location)

        message = "Alert! A " + threat_level + " " + threat_class + " has been reported at " + location + " at " + current_time + ". Nearest hospital is " + hospital + ". Stay safe!"

        # Send a WhatsApp Message to the contact instantly (gives 10s to load web client before sending)
        number = "+" + str(number)
        pywhatkit.sendwhatmsg_instantly(number, message, 10)

        pyautogui.click(1335,740)
        # time.sleep(4)
        # k.press_and_release('enter')

    def send_fire_msg(self, location, threat_level, threat_class):

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        data = [['Manipal', +919136339052], ['Chennai', +918420856104], ['Pune', +919820218571]]
        fire = pd.DataFrame(data, columns=['Location', 'Number']) 

        number = fire.loc[fire['Location'] == location].Number
        fnum = number[0]

        message = "Fire Alert! A " + threat_level + " " + threat_class + " has been reported at " + location + " at " + current_time + "."

        # Send a WhatsApp Message to the contact instantly (gives 10s to load web client before sending)
        number = "+" + str(number)
        pywhatkit.sendwhatmsg_instantly(number, message, 10)

        pyautogui.click(1335,740)
        # time.sleep(4)
        # k.press_and_release('enter')

# def main():
#     # number = input("Enter phone number (including country code): ")
#     location = input("Enter location: ")
#     threat_level = input("Enter threat level: ")
#     threat_class = input("Enter threat class: ")

#     obj = alerter()
#     obj.send_msg(location, threat_level, threat_class)

#     # if threat_class == 'Arson' or threat_class == 'RoadAccidents':
#     #     obj.send_fire_msg(location, threat_level, threat_class)

# if __name__ == '__main__':
#     main()