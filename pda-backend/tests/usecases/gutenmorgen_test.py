import pytest

from proaktiv_sender import ProaktivSender
from settings_manager import SettingsManager
from scheduler import Scheduler
from usecases.gutenmorgen import GutenMorgenUseCase
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

SETTINGS = {"goodMorning":{
                "homeAddress": "Segelfalterstrasse 2, 70439 Stuttgart",
                "modeOfTransportation": "bicycling",
                "name": "Max Mustermann",
                "workAddress": "Lerchenstrasse 1, 70176 Stuttgart"
            }}

@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
@patch.object(GutenMorgenUseCase, "get_work_time", return_value=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
@patch.object(Scheduler, "schedule_job", return_value=MagicMock())
def test_trigger(mock_scheduler, mock_work_time, mock_travel_time):
    usecase = GutenMorgenUseCase(Scheduler(), MagicMock(), MagicMock())
    mock_work_time.assert_called_once()
    mock_travel_time.assert_called_once()
    schedule_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    assert schedule_time == mock_scheduler.call_args.args[1]


@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
@patch.object(GutenMorgenUseCase, "get_work_time", return_value=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
@patch.object(ProaktivSender, "send_text")
def test_alarm(mock_proaktiv, mock_work_time, mock_travel_time):
    usecase = GutenMorgenUseCase(MagicMock(), MagicMock(), ProaktivSender(MagicMock))
    usecase.alarm()
    print(mock_proaktiv.call_args.args)
    assert any("You should leave at 08:25 to get to work at 09:00 on time!" in argument for argument in mock_proaktiv.call_args.args)

@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
def test_greeting(mock_settings, mock_travel_time):
    usecase = GutenMorgenUseCase(MagicMock(), SettingsManager(""), MagicMock())
    text = usecase.greeting()
    name = usecase.get_settings()["name"]
    assert name in text

@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_start_question(mock_travel_time):
    usecase = GutenMorgenUseCase(MagicMock(), MagicMock(), MagicMock())
    text = usecase.start_question()
    assert type(text) == str

@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_repeat_question(mock_travel_time):
    usecase = GutenMorgenUseCase(MagicMock(), MagicMock(), MagicMock())
    text = usecase.repeat_question()
    assert type(text) == str

@patch("services.weather.get_weather_forecast", return_value=(0, 1, "rain"))
@patch("services.weather.get_current_weather", return_value=(0, "LOCATION", "rain"))
@patch("services.geolocation.get_location_from_address", return_value=(48.777, 9.177))
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_weather(mock_travel_time, mock_settings, mock_geolocation, mock_weather, mock_forecast):
    usecase = GutenMorgenUseCase(MagicMock(), SettingsManager(""), MagicMock())
    text = usecase.weather()
    assert text == "It is currently 0 degrees celsius in LOCATION with rain. \
				Today, the forecast calls for a low of 0 and a high of 1 degrees, with rain in the afternoon."
    mock_geolocation.assert_called_once_with("Segelfalterstrasse 2, 70439 Stuttgart")
    mock_weather.assert_called_once()
    mock_forecast.assert_called_once()

@patch("services.news.get_news_title", return_value="NEWS STORY")
@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_news(mock_travel_time, mock_news_title):
    usecase = GutenMorgenUseCase(MagicMock(), MagicMock(), MagicMock())
    text = usecase.news_title()
    assert "NEWS STORY" in text
    mock_news_title.assert_called_once()

@patch("services.weather.get_weather_code", return_value=401)
@patch("services.geolocation.get_location_from_address", return_value=(48.777, 9.177))
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
@patch.object(GutenMorgenUseCase, "get_travel_time", return_value=30)
@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_travel_helper(mock_cached_travel_time, mock_current_travel_time, mock_settings, mock_geolocation, mock_weather_code):
    usecase = GutenMorgenUseCase(MagicMock(), SettingsManager(""), MagicMock())
    text, new_mode = usecase.travel_helper()
    assert new_mode == "driving"
    mock_geolocation.assert_called_once_with("Segelfalterstrasse 2, 70439 Stuttgart")
    mock_weather_code.assert_called_once()

@patch.object(GutenMorgenUseCase, "get_travel_time", return_value=30)
@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_travel_format(mock_cached_travel_time, mock_current_travel_time):
    usecase = GutenMorgenUseCase(MagicMock(), MagicMock(), MagicMock())
    mode = usecase.get_settings()["modeOfTransportation"]
    text = usecase.travel_time_format(mode)
    assert "30 minutes to get to work" in text
    mock_current_travel_time.assert_called_once()

@patch("services.maps.get_current_travel_time", return_value=30*60)
@patch.object(SettingsManager, "get_all_settings", return_value=SETTINGS)
@patch.object(GutenMorgenUseCase, "get_cached_travel_time", return_value=30)
def test_get_travel_time(mock_cached_travel_time, mock_settings, mock_travel_time):
    usecase =  GutenMorgenUseCase(MagicMock(), SettingsManager(""), MagicMock())
    mode = usecase.get_settings()["modeOfTransportation"]
    time = usecase.get_travel_time(mode)
    assert time == 30
    mock_travel_time.assert_called_once()