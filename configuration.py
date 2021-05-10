import os

# Platfrom should be picked based on OS (MacOS, Ubuntu etc.)
# It should be configurable based on user's input or picked automatically
class Configuration:
	def __init__(self):
		pass

	@property
	def platform(self):
		if self._platform:
			return self._platform
		else:
			return os.name

	@platform.setter
	def platform(self, new_platform):
		self._platform = new_platfrom


