from service_actions.base_service import BaseService
import json


class ConfigurationService(BaseService):
	def __init__(self, installer):
		super().__init__(installer)

		self.config = installer.config
		self.config_path = self.config.config_path
		self.load()

	def _call(self):
		self.config.items["app_manager"] = input("app manager (brew | aptget): ")

		self.save()

	def load(self):
		with open(self.config_path, "r") as f:
			config = f.read()

			self.config.items = json.loads(config)

	def save(self):
		with open(self.config_path, "w") as f:
			f.write(json.dumps(self.config.items))

