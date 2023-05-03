from geopy.geocoders import Nominatim
from geopy.distance import geodesic


geolocator = Nominatim(user_agent="my-app")

# the .latitude and .longitude is what fetches the actual figures
hub_location = (9.08622, 7.48128)


spoke_location = (9.09418, 7.49553)


distance = geodesic(hub_location, spoke_location).km

print(distance) # Output: 5566.8 km