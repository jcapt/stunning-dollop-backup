from service import Service
from service_actions.base_service import BaseService
from brew import Homebrew


class AddService(BaseService):
	def _call(self):
		# TODO don't require install command, define default package managers like brew, apt-get
		# then add default commands for managers
		install_command = self.command.install_command
		name = self.command.name
		self.add_service(name, install_command)

	def add_service(self, name, install_command):
		service = Service(name, install_command)
		self.services.append(service)
		self.database.add_entry(*service.to_db())


