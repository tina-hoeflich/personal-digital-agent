import json

class SettingsManager():
	"""Settings manager for managing all user settings"""

	CACHE: dict = {}
	FILENAME = ''

	def __init__(self, filename: str):
		"""Initialize the settings manager

		Args:
			filename (str): name of the settings file
		"""
		self.FILENAME = filename

	def save_settings(self, settings: dict):
		"""Save the settings to a file

		Args:
			settings (dict): settings to save
		"""
		self.CACHE.clear()
		self.CACHE.update(settings)
		with open(self.FILENAME, 'w') as f:
			json.dump(settings, f, indent=4)
		return "Success"

	def save_setting_by_name(self, name: str, value: object):
		"""Save a setting by its name

		Args:
			name (str): name of the setting
			value (object): value of the setting
		"""
		temp = self.CACHE.copy()
		temp.update({name: value})
		self.save_settings(temp)

	def get_all_settings(self) -> dict:
		"""Get the settings from a file

		Returns:
			dict: settings
		"""
		if self.CACHE:
			return self.CACHE
		with open(self.FILENAME, 'r') as f:
			data = json.load(f)
			self.CACHE.update(data)
			return data

	def get_setting_by_name(self, name: str) -> object:
		"""Get a setting by its name

		Args:
			name (str): name of the setting

		Returns:
			object: setting
		"""
		return self.get_all_settings()[name]
