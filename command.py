import sys
from logger import logger


class Command():
	def __init__(self):
		self.command_argv = sys.argv

	@property
	def action(self):
		base = self.command_argv[1].strip()
		logger.info(f"PARSER:ACTION {base}")
		return base

	@property
	def name(self):
		base = self.command_argv[2].strip()
		logger.info(f"PARSER:SERVICE_NAME {base}")
		return base

	@property
	def install_command(self):
		base = self.command_argv[3].strip()
		logger.info(f"PARSER:INSTALL_COMMAND {base}")
		return base
