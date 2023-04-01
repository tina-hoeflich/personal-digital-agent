from settings_manager import SettingsManager
from usecases.sparsupport import SparenUseCase
from unittest.mock import Mock, patch, MagicMock

SETTINGS = {"goodMorning": {"homeAddress": "Segelfalterstrasse 2, 70439, Stuttgart"},
			"sparen": {"stocks": {"favorites": [{"symbol": "AAPL", "priceHigh": 100, "priceLow": 50}]},
					   "sprit": {"typ": "e10", "radius": 10, "limit": 1.500}}}


@patch("services.tankerkoenig.get_fuelprice", return_value=("LOCATION", 1.000))
@patch("services.geolocation.get_location_from_address", return_value=(48.777, 9.177))
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_fuelprice_text_below(mock_settings, mock_geolockation, mock_fuelprice):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_fuelprice_text(True)
	mock_geolockation.assert_called_once_with("Segelfalterstrasse 2, 70439, Stuttgart")
	assert text == "The currently lowest e10 fuel price is 1.000€ at LOCATION. This is below your set limit of 1.500€. " \
				   "You should go there and fill up!"


@patch("services.tankerkoenig.get_fuelprice", return_value=("LOCATION", 3.000))
@patch("services.geolocation.get_location_from_address", return_value=(48.777, 9.177))
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_fuelprice_text_above(mock_settings, mock_geolockation, mock_fuelprice):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_fuelprice_text(True)
	mock_geolockation.assert_called_once_with("Segelfalterstrasse 2, 70439, Stuttgart")
	assert text == "The currently lowest e10 fuel price is 3.000€ at LOCATION. This is above your set limit of " \
				   "1.500€. Maybe you should wait fueling your car until it is cheaper!"
