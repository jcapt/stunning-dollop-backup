import sys, argparse
from logger import logger

def setup_parser(command):
	parser = argparse.ArgumentParser(description='Dollop - App reinstaller')

	parser.add_argument('--brew')
	parser.add_argument('--aptget')

	parser.add_argument('action', choices=['configuration', 'info', 'add', 'list', 'remove', 'install'])

	parser.add_argument('--name')
	parser.add_argument('--install_command')

	command.parser = parser
	command.args = parser.parse_args()
	logger.info(f"ARGPARSE {command.args}")


class Command():
	def __init__(self):
		setup_parser(self)

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

