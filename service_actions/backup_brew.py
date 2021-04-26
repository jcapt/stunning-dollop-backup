from service_actions.base_service import BaseService
from brew import Homebrew


class BackupBrewService(BaseService):
	def _call(self):
		brew = Homebrew()
		services = brew.load_brew()
		for service in services:
			# TODO don't do both actions
			self.services.append(service)

