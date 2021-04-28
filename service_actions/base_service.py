class BaseService():
	def __init__(self, installer):
		self.installer = installer
		# TODO: FIX IT, looks really bad
		self.database = installer.database
		self.services = installer.services
		self.command = installer.command

	@classmethod
	def call(cls, installer):
		return cls(installer)._call()

	def _call(self):
		raise BaseException("Not implemented error")

	def get_service(self, name):
		services_list = [service for service in self.services if service.name == name]
		if len(services_list) > 0:
			return services_list[0]

