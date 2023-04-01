import requests
import json

# enter the location you want to search around
location = input("Enter location: ")
#working for manipal, chennai

# create the API request URL
url = "https://nominatim.openstreetmap.org/search?q={0}&format=json&limit=1".format(location)

# send the API request
response = requests.get(url)

# parse the JSON response
data = json.loads(response.text)
# print(data)
# # extract the latitude and longitude of the location
lat = data[0]["lat"]
lon = data[0]["lon"]

# # create the API request URL to search for police stations near the location
urlp = "https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=police](around:500,{0},{1});out;".format(lat, lon)
urlh = "https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=hospital](around:500,{0},{1});out;".format(lat, lon)
# # send the API request
responsep = requests.get(urlp)
responseh = requests.get(urlh)
# # parse the JSON response
datap = json.loads(responsep.text)
datah = json.loads(responseh.text)
# print(data)
# # extract the nearest police station's name and address
pname = datap["elements"][0]["tags"]["name"]
hname = datah["elements"][0]["tags"]["name"]
# address = data["elements"][0]["tags"]["addr:full"]

# # print the nearest police station's name and address
print("Nearest police station: {0}".format(pname))
print("Nearest hospital: {0}".format(hname))
# print("Address: {0}".format(address))
