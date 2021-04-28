import sys, argparse
from logger import logger


class Command():
	def __init__(self):
		self.command_argv = sys.argv
		self.parser = argparse.ArgumentParser(description='Dollop - App reinstaller')
		self.parser.add_argument('--brew', action='store_true')
		self.parser.add_argument('--aptget', action='store_true')
		self.parser.add_argument('action')
		self.parser.add_argument('--name')
		self.parser.add_argument('--install_command')
		self.args = self.parser.parse_args()
		logger.info(f"ARGPARSE {self.args}")

	@property
	def action(self):
		base = self.args.action
		logger.info(f"PARSER:ACTION => {base}")
		return base

	@property
	def name(self):
		base = self.args.name
		logger.info(f"PARSER:SERVICE_NAME => {base}")
		return base

	@property
	def install_command(self):
		if self.args.brew:
			base = self.brew_default_command()
		elif self.args.aptget:
			base = self.aptget_default_command()
		else:
			base = self.args.install_command

		logger.info(f"PARSER:INSTALL_COMMAND => {base}")
		return base

	def brew_default_command(self):
		return f"brew install {self.name}"

	def aptget_default_command(self):
		return f"sudo apt-get install {self.name}"

