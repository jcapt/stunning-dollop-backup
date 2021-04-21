import sys, re
from database import Database
from service import Service
from command import Command

from service_actions.add import AddService
from service_actions.remove import RemoveService
from service_actions.install import InstallService
from service_actions.list import ListService
from service_actions.info import InfoService
from service_actions.backup_brew import BackupBrewService

from service_database.rebalancer import Rebalancer

ACTIONS = ["add", "remove", "install", "list", "info", "backup_brew"]
ACTIONS_TO_SERVICES = {
		"add": AddService,
		"remove": RemoveService,
		"install": InstallService,
		"list": ListService,
		"info": InfoService,
		"backup_brew": BackupBrewService
}

class ServicesProxy(list):
	def append(self, service):
		super(service)

	def remove(self, service):
		super(service)

proxy = ServicesProxy()
print(proxy)

for service in proxy:
	print(service)


class Installer:
	def __init__(self):
		self._services = []
		self.database = Database()
		self.database.add_extension(Rebalancer)
		self.command = Command()

	@property
	def services(self):
		return self._services

	@services.setter
	def services(self, services):
		self._services = services

	# TODO: add platform picker? so one backup can be suited for syncing data like mackup (lra/mackup)
	def main(self):
		action = self.command.action

		if self.validate_action(action):
			self.load_from_database()

			ACTIONS_TO_SERVICES[action].call(self)

			self.database.save()

	def load_from_database(self):
		for entry in self.database.entries:
			self.services.append(Service.from_database(entry))

	def validate_action(self, action):
		return action in ACTIONS

