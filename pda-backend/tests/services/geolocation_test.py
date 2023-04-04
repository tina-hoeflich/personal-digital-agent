import services.geolocation as geolocation


def tests_geolocation():
	lat, lng = geolocation.get_location_from_address("Porscheplatz 1, Stuttgart, Germany")
	assert type(lat) == float
	assert type(lng) == float
	#48.834909589444884, 9.152177970447948
	assert lat > 48.833
	assert lat < 48.835
	assert lng > 9.152
	assert lng < 9.153
