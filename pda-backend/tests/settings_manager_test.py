from unittest.mock import patch, mock_open
from settings_manager import SettingsManager

SETTINGS_JSON = '{"example": {"name": "test"} }'


@patch("builtins.open", new_callable=mock_open, read_data=SETTINGS_JSON)
def test_readsettings(mock_file):
	settings_manager = SettingsManager("settings.json")
	settings = settings_manager.get_all_settings()
	assert settings["example"]["name"] == "test"
	named_settings = settings_manager.get_setting_by_name("example")
	assert named_settings["name"] == "test"

	mock_file.assert_called_once_with("settings.json", "r")

@patch("builtins.open", new_callable=mock_open, read_data=SETTINGS_JSON)
def test_writesettings(mock_file):
	settings_manager = SettingsManager("settings.json")
	_ = settings_manager.get_all_settings()
	settings_manager.save_setting_by_name("example", {"name": "test2"})
	settings = settings_manager.get_setting_by_name("example")
	assert settings["name"] == "test2"

	assert mock_file.call_count == 2
