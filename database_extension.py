from logger import logger

def extensions_stack(func):
	def wrapper(*args):
		database = args[0]
		func_name = func.__name__

		args_list = list(args)

		database.run_extensions_before(func_name, args_list)
		res = func(*args_list)
		database.run_extensions_after(func_name, args_list)

		return res

	return wrapper


class DatabaseExtension():
	def add_extension(self, extension):
		return self.extensions.append(extension(self))

	def remove_extension(self, extension):
		return self.extensions.remove(extension(self))

	def run_extensions_before(self, func_name, args_list):
		logger.info(f"DATABASE:EXTENSIONS:BEFORE {func_name}")
		for extension in self.extensions:
			extension.run_before(func_name, args_list)

	def run_extensions_after(self, func_name, args_list):
		logger.info(f"DATABASE:EXTENSIONS:AFTER {func_name}")
		for extension in self.extensions:
			extension.run_after(func_name, args_list)

