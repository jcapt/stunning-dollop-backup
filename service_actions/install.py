from service_actions.base_service import BaseService


class InstallService(BaseService):
	def _call(self):
		if self.command.name:
			service = self.get_service(self.command.name)
			service.install()
		else:
			for service in self.services:
				service.install()

