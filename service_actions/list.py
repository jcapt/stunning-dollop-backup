from service_actions.base_service import BaseService


class ListService(BaseService):
	def _call(self):
		print("INSTALLED SERVICES:")
		for service in self.services:
			print(service.name)

