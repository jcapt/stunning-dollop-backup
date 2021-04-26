class ServicesProxy():
	def __init__(self, database, data):
		self._data = data
		self.database = database

	def append(self, service):
		self.raw_append(service)
		self.database.add_entry(*service.to_db())

	def raw_append(self, service):
		self._data.append(service)

	def remove(self, service):
		self.database.remove_entry(service.name)

	def raw_remove(self, service):
		self._data.remove(service)

	def __iter__(self):
		for elem in self._data:
			yield elem

