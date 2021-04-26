from logger import logger


class Rebalancer():
	def __init__(self, database):
		self.database = database
		self.add_count = 0

	def run_before(self, func_name, *args):
		return
		if func_name == "add_entry":
			logger.info("DATABASE:REBALANCER:COUNT_UP")
			self.add_count = self.add_count + 1

	def run_after(self, func_name, *args):
		return
		if self.add_count == 25 and not func_name == "save":
			logger.info("DATABASE:REBALANCER:TRIGGER_SAVE")
			self.database.save()
			self.add_count = 0

