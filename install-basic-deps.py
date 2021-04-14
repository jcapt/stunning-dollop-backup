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


ACTIONS = ["add", "remove", "install", "list", "info", "backup_brew"]
ACTIONS_TO_SERVICES = { "add": AddService, "remove": RemoveService, "install": InstallService, "list": ListService, "info": InfoService, "backup_brew": BackupBrewService }


class Installer:
	def __init__(self):
		# TODO: Don't store services in array, use models
		self.services = []
		self.database = Database()
		self.command = Command()

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

installer = Installer()

installer.main()

