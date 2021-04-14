from service_actions.base_service import BaseService


class InfoService(BaseService):
	def _call(self):
		name = self.command.name
		print(self.get_service(name).get_info())

