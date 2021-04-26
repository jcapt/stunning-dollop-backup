import os


class PlatformSaver():
	def __init__(self, database):
		self.database = database

	def run_before(self, func_name, args):
		if func_name == "add_entry":
			database_value = args[2]
			database_value["platform"] = os.name
			args[2] = database_value

	def run_after(self, func_name, args):
		pass

