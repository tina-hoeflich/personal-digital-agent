import pytest

from proaktiv_sender import ProaktivSender
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


@patch("services.stocks.get_stock_price", return_value=10000)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_stockprice_text_above(mock_settings, mock_stocks):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_stockprice_text(True)
	assert text == "The stock price of AAPL is 10000.00€. This is above your set limit of 100.00€. This is looking great! You will be rich soon!\n"
	mock_stocks.assert_called_once_with("AAPL")
	mock_settings.assert_called_once()

@patch("services.stocks.get_stock_price", return_value=10)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_stockprice_text_below(mock_settings, mock_stocks):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_stockprice_text(True)
	assert text == "The stock price of AAPL is 10.00€. This is below your set limit of 50.00€. Maybe you should sell all your stocks now!\n"
	mock_stocks.assert_called_once_with("AAPL")
	mock_settings.assert_called_once()


@patch("services.stocks.get_stock_price", return_value=75)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_stockprice_text_inside(mock_settings, mock_stocks):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_stockprice_text(True)
	assert text == "The stock price of AAPL is 75.00€. This is not above or below your limits\n"
	mock_stocks.assert_called_once_with("AAPL")
	mock_settings.assert_called_once()


@patch.object(SparenUseCase, "get_stockprice_text", return_value="Stock_return")
@patch.object(SparenUseCase, "get_fuelprice_text", return_value="Fuel_return")
@patch.object(ProaktivSender, "send_text")
def test_trigger(mock_proaktiv, mock_fuel, mock_stock):
	usecase = SparenUseCase(MagicMock(), MagicMock(), ProaktivSender(MagicMock()))
	usecase.trigger()
	mock_fuel.assert_called_once()
	mock_stock.assert_called_once()
	assert any("Stock_return" in argument for argument in mock_proaktiv.call_args.args)
	assert any("Fuel_return" in argument for argument in mock_proaktiv.call_args.args)

@pytest.mark.asyncio
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
@patch.object(SparenUseCase, "get_fuelprice", return_value=["unused", 2.0])
async def test_asked(mock_fuelprice, _):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	output, _ = await usecase.asked("")
	assert "Do you want to hear it?" in output
	assert "stock" in output
	mock_fuelprice.assert_called_once()
