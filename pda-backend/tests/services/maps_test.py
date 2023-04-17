import services.maps as maps
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

SETTINGS = {"goodMorning":{
                "homeAddress": "Segelfalterstrasse 2, 70439 Stuttgart",
                "modeOfTransportation": "bicycling",
                "name": "Max Mustermann",
                "workAddress": "Lerchenstrasse 1, 70176 Stuttgart"
            }}

mock_maps_data = {"data": [{"legs": [{"duration": {"value": 10}, "duration_in_traffic": {"value": 10}}]}]}

@patch("services.maps.refresh_cache", return_value=None)
def test_get_and_refresh_cache(mock_cache_refresher):
    current_date = datetime.today().strftime('%Y-%m-%d')
    frm = SETTINGS["goodMorning"]["homeAddress"]
    to = SETTINGS["goodMorning"]["workAddress"]
    mode = SETTINGS["goodMorning"]["modeOfTransportation"]
    cache_data = maps.get_and_refresh_cache(frm, to, mode)
    
    assert cache_data["parameters"]["date"] == current_date
    assert cache_data["data"][0]["legs"][0]["start_address"] == "Segelfalterstraße 2, 70439 Stuttgart, Germany"
    assert cache_data["data"][0]["legs"][0]["end_address"] == "Lerchenstraße 1, 70174 Stuttgart, Germany"
    assert cache_data["data"][0]["legs"][0]["steps"][0]["travel_mode"] == "BICYCLING"

def test_get_current_data():
    current_date = datetime.today().strftime('%Y-%m-%d')
    frm = SETTINGS["goodMorning"]["homeAddress"]
    to = SETTINGS["goodMorning"]["workAddress"]
    mode = SETTINGS["goodMorning"]["modeOfTransportation"]
    cache_data = maps.get_current_data(frm, to, mode)
    
    assert cache_data["parameters"]["date"] == current_date
    assert cache_data["data"][0]["legs"][0]["start_address"] == "Segelfalterstraße 2, 70439 Stuttgart, Germany"
    assert cache_data["data"][0]["legs"][0]["end_address"] == "Lerchenstraße 1, 70174 Stuttgart, Germany"
    assert cache_data["data"][0]["legs"][0]["steps"][0]["travel_mode"] == "BICYCLING"

@patch("services.maps.get_and_refresh_cache", return_value = mock_maps_data)
def test_get_cached_travel_time(mock_data_getter):
    frm = SETTINGS["goodMorning"]["homeAddress"]
    to = SETTINGS["goodMorning"]["workAddress"]
    mode = SETTINGS["goodMorning"]["modeOfTransportation"]
    time = maps.get_cached_travel_time(frm, to, mode)
    assert time == 10
    mock_data_getter.assert_called_once()

@patch("services.maps.get_current_data", return_value = mock_maps_data)
@patch("services.maps.refresh_cache", return_value=None)
def test_get_current_travel_time(mock_cache_refresher, mock_data_getter):
    frm = SETTINGS["goodMorning"]["homeAddress"]
    to = SETTINGS["goodMorning"]["workAddress"]
    mode = SETTINGS["goodMorning"]["modeOfTransportation"]
    time = maps.get_current_travel_time(frm, to, mode)
    assert time == 10
    mock_cache_refresher.assert_called_once()
    mock_data_getter.assert_called_once()