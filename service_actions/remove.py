from service_actions.base_service import BaseService


class RemoveService(BaseService):
	def _call(self):
		self.remove_service(self.command.name)

	def remove_service(self, name):
		service = self.get_service(name)
		if service:
			self.services.remove(service)

