import geocoder
from geopy.geocoders import Nominatim

g = geocoder.ip('me')

geoloc = Nominatim(user_agent="GetLoc")

latlong = g.latlng

ltlg = ', '.join(str(e) for e in latlong)
print(type(ltlg))
locname = geoloc.reverse(latlong)
locdetails = ' '.join(str(e) for e in locname)
print(type(locdetails))
