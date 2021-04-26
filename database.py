import re
from logger import logger
import hashlib
from checksum import get_checksum
from database_extension import DatabaseExtension, extensions_stack
import json

def database_check(func):
	def wrapper(*args):
		database = args[0]
		if not database.loaded:
			database.load()

		return func(*args)

	return wrapper


class Database(DatabaseExtension):
	def __init__(self):
		self.path = "./_database"
		self._entries = []
		self.loaded = False
		self.hashsum = 0
		self.extensions = []

	@property
	@database_check
	def entries(self):
		return self._entries

	@entries.setter
	def entries(self, entries):
		self._entries = entries

	@database_check
	@extensions_stack
	def add_entry(self, key, service):
		if not self.get_entry(key):
			logger.info(f"DATABASE:ADD {key}, {service}")
			self.entries.append([key, json.dumps(service)])

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
				root_data = ""
				# TODO: don't resave each database entry, only entries that changed
				for entry in self.entries:
					key = entry[0]
					data = entry[1].encode('utf-8').hex()
					root_data = root_data + f"{key},{data}\n"

				f.write(root_data.encode('utf-8').hex())


	@extensions_stack
	def load(self):
		logger.info("DATABASE:LOAD")
		with open(self.path, "r") as f:
			database_string = f.read()
			raw_database = bytearray.fromhex(database_string).decode()

			self.entries = self.process_entries(raw_database)
			self.loaded = True

			self.hashsum = get_checksum(self.entries)
			logger.debug(f"DATABASE:HASHSUM => {self.hashsum}")

	def hashsum_changed(self):
		new_hashsum = get_checksum(self.entries)
		check = new_hashsum != self.hashsum
		logger.debug(f"DATABASE:CHECK_HASHSUM ({new_hashsum} != {self.hashsum}) => {check}")
		return check

