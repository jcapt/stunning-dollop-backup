from service_actions.base_service import BaseService


class BackupBrewService(BaseService):
	def _call(self):
		brew = Homebrew()
		services = brew.load_brew()
		for service in services:
			self.services.append(service)
			self.database.add_entry(*service.to_db())

