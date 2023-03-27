import geopy

def get_location_from_address(address: str) -> tuple[float, float]:
	"""Get the location of a given address

	Args:
		address (str): address to get the location for

	Returns:
		tuple[float, float]: the latitude and longitude of the given address
	"""
	geolocator = geopy.geocoders.Nominatim(user_agent="PersonalDigitalAssistant DHBW Stuttgart 20ITA")
	location = geolocator.geocode(address)
	return location.latitude, location.longitude
