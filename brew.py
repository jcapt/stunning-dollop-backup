import os
from service import Service
from logger import logger


class Homebrew():
	def __init__(self):
		self.leaves = []
		self.casks = []
		self.services = []

	def load_brew(self):
		self.load_leaves()

		for leave in self.leaves:
			self.services.append(Service(leave, f"brew install {leave}", metadata={'fromBrew': True}))

		return self.services

	def load_leaves(self):
		logger.info("HOMEBREW:LOAD_LEAVES")
		res = os.system("brew leaves > leaves.tmp")
		if res == 0:
			with open("leaves.tmp", "r") as f:
				res1 = f.read()
				res1 = res1.split("\n")
				for entry in res1:
					if entry:
						self.leaves.append(entry)

		os.system("rm leaves.tmp")

