from service_actions.base_service import BaseService


class InstallService(BaseService):
	def _call(self):
		for service in self.services:
			service.install()

