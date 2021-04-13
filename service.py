import subprocess, logging, json, datetime


class Service:
	def __init__(self, name, install_command, metadata={}, saved=False):
		self.name = name
		self.install_command = install_command
		self.metadata = metadata
		self.saved = saved

	def __repr__(self):
		return f"Service(name={self.name})"

	@classmethod
	def from_database(cls, database_entry):
		name = database_entry[0]
		data = json.loads(database_entry[1])
		install_command = data.pop("install_command", None)
		return cls(name, install_command, metadata=data, saved=True)

	def install(self):
		logging.info(f"INSTALLER:INSTALL {self.name}")
		subprocess.run(self.install_command.split(" "))

	# TODO: save platform eg mac, ubuntu
	def to_db(self):
		metadata = self.metadata
		metadata["install_command"] = self.install_command
		self.metadata["created_at"] = datetime.datetime.now().isoformat()
		return [self.name, json.dumps(metadata)]

	def get_info(self):
		return f"COMMAND: {self.install_command} \nMETADATA: {self.metadata}"
