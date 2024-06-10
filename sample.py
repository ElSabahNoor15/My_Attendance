import geocoder
from geopy.geocoders import Nominatim

g = geocoder.ip('me')

geoloc = Nominatim(user_agent="GetLoc")

latlong = g.latlng

ltlg = ', '.join(str(e) for e in latlong)
#print(ltlg)
locname = geoloc.reverse(latlong)
locdetails = ' '.join(str(e) for e in locname)
#print(locdetails)

import json
from urllib.request import urlopen

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
print(data['loc'])
print(type(data['loc']))