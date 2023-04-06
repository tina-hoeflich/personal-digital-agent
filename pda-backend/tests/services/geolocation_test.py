from unittest.mock import patch

from geopy import Nominatim, Location, Point

import services.geolocation as geolocation


@patch.object(Nominatim, "geocode", return_value=Location("", Point(48.8339945, 9.15235), ""))
def tests_geolocation(mock_geocode):
	lat, lng = geolocation.get_location_from_address("Porscheplatz 1, Stuttgart, Germany")
	assert type(lat) == float
	assert type(lng) == float
	#48.834909589444884, 9.152177970447948
	assert lat > 48.833
	assert lat < 48.835
	assert lng > 9.152
	assert lng < 9.153

	assert mock_geocode.assert_called_once
