from geopy.geocoders import Nominatim
from geopy.distance import geodesic


geolocator = Nominatim(user_agent="my-app")

location_1 = geolocator.geocode("New York")
location_2 = geolocator.geocode("London")

print(location_1)
print(location_2)

# the .latitude and .longitude is what fetches the actual figures
ny_location = (location_1.latitude, location_1.longitude)
print(ny_location)

london_location = (location_2.latitude, location_2.longitude)
print(london_location)


distance = geodesic(ny_location, london_location).km

print(distance) # Output: 5566.8 km