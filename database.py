import re
from logger import logger
import hashlib
from checksum import get_checksum

def database_check(func):
	def wrapper(*args):
		database = args[0]
		if not database.loaded:
			database.load()

		return func(*args)

	return wrapper

def extensions_stack(func):
	def wrapper(*args):
		database = args[0]

		database.run_extensions_before(func.__name__)
		res = func(*args)
		database.run_extensions_after(func.__name__)

		return res

	return wrapper


class Database:
	def __init__(self):
		self.path = "./_database"
		self._entries = []
		self.loaded = False
		self.hashsum = 0
		self.extensions = []

	def add_extension(self, extension):
		return self.extensions.append(extension(self))

	def remove_extension(self, extension):
		return self.extensions.remove(extension(self))

	def run_extensions_before(self, func_name):
		logger.info(f"DATABASE:EXTENSIONS:BEFORE {func_name}")
		for extension in self.extensions:
			extension.run_before(func_name)

	def run_extensions_after(self, func_name):
		logger.info(f"DATABASE:EXTENSIONS:AFTER {func_name}")
		for extension in self.extensions:
			extension.run_after(func_name)

	@property
	@database_check
	def entries(self):
		return self._entries

	@entries.setter
	def entries(self, entries):
		self._entries = entries

	@database_check
	@extensions_stack
	def add_entry(self, key, value):
		if not self.get_entry(key):
			logger.info(f"DATABASE:ADD {key}")
			self.entries.append([key, value])

	@database_check
	@extensions_stack
	def remove_entry(self, key):
		entry = self.get_entry(key)
		if entry:
			logger.info(f"DATABASE:REMOVE {key}")
			self.entries.remove(entry)

	@database_check
	@extensions_stack
	def get_entry(self, key):
		entries_list = [entry for entry in self.entries if entry[0] == key]
		if len(entries_list) > 0:
			return entries_list[0]

	def process_entries(self, raw_database):
		database = raw_database.split("\n")
		encoded_entries = [entry.split(",") for entry in database if len(entry) > 0]
		entries = []
		for encoded_entry in encoded_entries:
			entries.append([encoded_entry[0], bytearray.fromhex(encoded_entry[1]).decode()])

		return entries

	@extensions_stack
	def save(self):
		if self.hashsum_changed():
			logger.info("DATABASE:SAVE")
			with open(self.path, "w") as f:
				# TODO: don't resave each database entry, only entries that changed
				for entry in self.entries:
					key = entry[0]
					data = entry[1].encode('utf-8').hex()
					f.write(f"{key},{data}\n")

	@extensions_stack
	def load(self):
		logger.info("DATABASE:LOAD")
		with open(self.path, "r") as f:
			raw_database = f.read()

			self.entries = self.process_entries(raw_database)
			self.loaded = True

			self.hashsum = get_checksum(self.entries)
			logger.debug(f"DATABASE#HASHSUM={self.hashsum}")

	def hashsum_changed(self):
		new_hashsum = get_checksum(self.entries)
		check = new_hashsum != self.hashsum
		logger.debug(f"DATABASE:CHECK_HASHSUM ({new_hashsum} != {self.hashsum}) => {check}")
		return check

