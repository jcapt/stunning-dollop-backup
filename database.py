import re

class Database:
	def __init__(self):
		self.path = "./_database"
		self.entries = []
		self.load()

	def add_entry(self, key, value):
		if not self.get_entry(key):
			print(f"ADDING TO DATABASE {key}")
			self.entries.append([key, value])

	def remove_entry(self, key):
		entry = self.get_entry(key)
		if entry:
			print(f"REMOVING FROM DATABASE: {key}")
			self.entries.remove(entry)


	def get_entry(self, key):
		entries_list = [entry for entry in self.entries if entry[0] == key]
		if len(entries_list) > 0:
			return entries_list[0]

	def process_db(self, raw_database):
		database = raw_database.split("\n")
		encoded_entries = [entry.split(",") for entry in database if len(entry) > 0]
		entries = []
		for encoded_entry in encoded_entries:
			entries.append([encoded_entry[0], bytearray.fromhex(encoded_entry[1]).decode()])

		return entries

	def save(self):
		with open(self.path, "w") as f:
			for entry in self.entries:
				key = entry[0]
				data = entry[1].encode('utf-8').hex()
				f.write(f"{key},{data}\n")

	def load(self):
		with open(self.path, "r") as f:
			raw_database = f.read()

			self.entries = self.process_db(raw_database)


