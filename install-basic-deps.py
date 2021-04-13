import sys, re
from database import Database
from service import Service
from logger import logger
from brew import Homebrew

ACTIONS = ["add", "remove", "install", "list", "info", "backup_brew"]


class Installer:
	def __init__(self):
		self.services = []
		self.db_path = "./installer"
		self.database = Database()

	# TODO: add platform picker? so one backup can be suited for syncing data like mackup (lra/mackup)
	def main(self):
		action = sys.argv[1]

		logger.info(f"PARSER:ACTION {action}")

		if self.validate_action(action):
			self.load_from_database()

			# TODO: pick action based on service/file name instead of simple If.
			# Put services in actions folder, and load it on startup to check what's available
			if action == "add":
				name = sys.argv[2].strip()
				logger.info(f"PARSER:SERVICE_NAME {name}")

				# TODO don't require install command, define default package managers like brew, apt-get
				# then add default commands for managers
				install_command = sys.argv[3].strip()
				self.add_service(name, install_command)
			elif action == "remove":
				name = sys.argv[2].strip()
				logger.info(f"PARSER:SERVICE_NAME {name}")

				self.remove_service(name)
			elif action == "install":
				self.install_services()
			elif action == "list":
				self.list_services()
			elif action == "info":
				name = sys.argv[2].strip()
				logger.info(f"PARSER:SERVICE_NAME {name}")
				self.info_service(name)
			elif action == "backup_brew":
				self.backup_brew()

			self.database.save()

	def add_service(self, name, install_command):
		service = Service(name, install_command)
		self.services.append(service)
		self.database.add_entry(*service.to_db())

	def remove_service(self, name):
		service = self.get_service(name)
		if service:
			self.services.remove(service)
			self.database.remove_entry(name)

	def install_services(self):
		for service in self.services:
			service.install()

	def load_from_database(self):
		for entry in self.database.entries:
			self.services.append(Service.from_database(entry))

	def get_service(self, name):
		services_list = [service for service in self.services if service.name == name]
		if len(services_list) > 0:
			return services_list[0]

	def list_services(self):
		print("INSTALLED SERVICES:")
		for service in self.services:
			print(service.name)

	def info_service(self, name):
		print(self.get_service(name).get_info())

	def backup_brew(self):
		brew = Homebrew()
		services = brew.load_brew()
		for service in services:
			self.services.append(service)
			self.database.add_entry(*service.to_db())

	def validate_action(self, action):
		return action in ACTIONS

installer = Installer()

installer.main()

