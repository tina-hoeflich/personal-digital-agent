import pytest

from proaktiv_sender import ProaktivSender
from settings_manager import SettingsManager
from usecases.sparsupport import SparenUseCase
from unittest.mock import patch, MagicMock

SETTINGS = {"goodMorning": {"homeAddress": "Segelfalterstrasse 2, 70439, Stuttgart"},
			"sparen": {"stocks": {"favorites": [{"symbol": "AAPL", "priceHigh": 100, "priceLow": 50}]},
					   "sprit": {"typ": "e10", "radius": 10, "preisschwelle": 1.500}}}


@patch("services.tankerkoenig.get_fuelprice", return_value=("LOCATION", 1.000))
@patch("services.geolocation.get_location_from_address", return_value=(48.777, 9.177))
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_fuelprice_text_below(mock_settings, mock_geolockation, mock_fuelprice):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_fuelprice_text(True)
	mock_geolockation.assert_called_once_with("Segelfalterstrasse 2, 70439, Stuttgart")
	assert "LOCATION" in text
	assert "e10" in text
	assert "1.000€" in text


@patch("services.tankerkoenig.get_fuelprice", return_value=("LOCATION", 3.000))
@patch("services.geolocation.get_location_from_address", return_value=(48.777, 9.177))
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_fuelprice_text_above(mock_settings, mock_geolockation, mock_fuelprice):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_fuelprice_text(True)
	mock_geolockation.assert_called_once_with("Segelfalterstrasse 2, 70439, Stuttgart")
	assert "LOCATION" in text
	assert "1.500€" in text
	assert "3.000€" in text


@patch("services.stocks.get_stock_price", return_value=10000)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_stockprice_text_above(mock_settings, mock_stocks):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_stockprice_text(True)
	assert "AAPL" in text
	assert "10000.00€" in text
	assert "100.00€" in text
	mock_stocks.assert_called_once_with("AAPL")
	mock_settings.assert_called_once()

@patch("services.stocks.get_stock_price", return_value=10)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_stockprice_text_below(mock_settings, mock_stocks):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_stockprice_text(True)
	assert "AAPL" in text
	assert "50.00€" in text
	assert "10.00€" in text
	mock_stocks.assert_called_once_with("AAPL")
	mock_settings.assert_called_once()


@patch("services.stocks.get_stock_price", return_value=75)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_stockprice_text_inside(mock_settings, mock_stocks):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	text = usecase.get_stockprice_text(True)
	assert "AAPL" in text
	assert "75.00€" in text
	mock_stocks.assert_called_once_with("AAPL")
	mock_settings.assert_called_once()


@patch.object(SparenUseCase, "get_general_text", return_value=["", True, False])
@patch.object(ProaktivSender, "send_text")
def test_trigger(mock_proaktiv, mock_general_text):
	usecase = SparenUseCase(MagicMock(), MagicMock(), ProaktivSender(MagicMock()))
	usecase.trigger()
	mock_general_text.assert_called_once()
	assert any("tips" in argument for argument in mock_proaktiv.call_args.args) or any("news" in argument for argument in mock_proaktiv.call_args.args)


@pytest.mark.asyncio
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
@patch.object(SparenUseCase, "get_fuelprice", return_value=["unused", 2.0])
async def test_asked(mock_fuelprice, _):
	usecase = SparenUseCase(MagicMock(), SettingsManager(""), MagicMock())
	output, _ = await usecase.asked("")
	assert "stock" in output
	mock_fuelprice.assert_called_once()
