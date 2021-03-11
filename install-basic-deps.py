import sys, re
from database import Database
from service import Service
import logging

database = Database()

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

logging.info("STARTING")


class Installer:
	def __init__(self):
		self.services = []
		self.db_path = "./installer"
		self.database = Database()
		self.load_from_database()

	def main(self):
		action = sys.argv[1]

		logging.info(f"ACTION: {action}")

		if action == "add":
			name = sys.argv[2].strip()
			logging.info(f"SERVICE_NAME: {name}")

			install_command = sys.argv[3].strip()
			self.add_service(name, install_command)
		elif action == "remove":
			name = sys.argv[2].strip()
			logging.info(f"SERVICE_NAME: {name}")

			self.remove_service(name)
		elif action == "install":
			self.install_services()
		elif action == "list":
			self.list_services()
		elif action == "info":
			name = sys.argv[2].strip()
			logging.info(f"SERVICE_NAME: {name}")
			self.info_service(name)

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


installer = Installer()

installer.main()

