from tkinter import BooleanVar, StringVar, IntVar
from configparser import ConfigParser
import os
import typing as T
from .module_manifest import ModuleManifest

class Parameters :
	def __init__(self, master = None):
		self.var_use_io_module = BooleanVar(master,False)
		self.var_use_os_module = BooleanVar(master,False)
		self.var_cleanup_debug_symbols = BooleanVar(master,True)
		self.var_use_links = BooleanVar(master,False)
		self.var_replace_main = BooleanVar(master,False)

		self.var_cproject_path = StringVar(master,None)
		self.var_sool_destination_path = StringVar(master,None)
		self.var_sool_path = StringVar(master, None)
		self.var_sool_chip = StringVar(master, None)

		self.modules_list : T.List[ModuleManifest] = list()

		self.read_parameters()

	def print(self):

		print("CProject  file : ", self.cproject_path)
		print("Sool dest path : ", self.sool_destination_path)
		print("SooL      path : ", self.sool_path)
		print("SooL Chip      : ", self.sool_chip)

	def read_parameters(self,path = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"):
		config_parser = ConfigParser()
		if os.path.exists(path) :
			config_parser.read(path)

		self.use_io_module = config_parser.getboolean("Modules","IO",fallback=False)
		self.use_os_module = config_parser.getboolean("Modules","OS", fallback=False)

		self.cleanup_debug_symbols = config_parser.getboolean("General","CleanupSymbols", fallback=True)
		self.use_links = config_parser.getboolean("General","UseLinks",fallback=False)
		self.replace_main = config_parser.getboolean("General","ReplaceMain",fallback=True)

		self.cproject_path = config_parser.get("Paths","CProject",fallback="")
		self.sool_destination_path = config_parser.get("Paths","SoolDestination", fallback="./sool")
		self.sool_path = config_parser.get("Paths","SoolSource", fallback="")
		self.sool_chip = config_parser.get("SooL","Chip", fallback="")
		self.modules_list = [ModuleManifest(x) for x in config_parser.get("Paths","SoolModules", fallback="").split(";") if os.path.exists(x) and os.path.isfile(x)]
		self.modules_selected_list = [ModuleManifest(x) for x in config_parser.get("Paths", "SoolModulesUsed", fallback="").split(";") if os.path.exists(x) and os.path.isfile(x)]

		for module in self.modules_list :
			module.read()
		for module in self.modules_selected_list :
			module.read()



	def write_parameters(self, path=os.path.dirname(os.path.abspath(__file__)) + "/config.ini"):
		config_parser = ConfigParser()

		config_parser.add_section("Modules")
		config_parser.add_section("General")
		config_parser.add_section("Paths")
		config_parser.add_section("SooL")

		config_parser.set("Modules","IO", 				str(self.use_io_module))
		config_parser.set("Modules","OS", 				str(self.use_os_module))

		config_parser.set("General","CleanupSymbols", 	str(self.cleanup_debug_symbols))
		config_parser.set("General","UseLinks",			str(self.use_links))
		config_parser.set("General","ReplaceMain",		str(self.replace_main))

		config_parser.set("Paths","CProject",			self.var_cproject_path.get())

		config_parser.set("Paths","SoolDestination", 	self.sool_destination_path)
		config_parser.set("Paths","SoolSource", 		self.sool_path)
		config_parser.set("SooL","Chip", 				self.sool_chip)
		config_parser.set("Paths","SoolModules", 		";".join([x.path for x in self.modules_list]))
		config_parser.set("Paths","SoolModulesUsed",	";".join([x.path for x in self.modules_selected_list]))

		with open(path,"w") as f :
			config_parser.write(f)

	@property
	def project_dir(self) -> str:
		return os.path.dirname(self.cproject_path)

	@property
	def project_sool_dir(self) -> str:
		return os.path.abspath(f"{self.project_dir}/{self.sool_destination_path}")

	@property
	def use_io_module(self) -> bool:
		return self.var_use_io_module.get()

	@use_io_module.setter
	def use_io_module(self,val : bool):
		self.var_use_io_module.set(val)
		
	@property
	def use_os_module(self) -> bool:
		return self.var_use_os_module.get()

	@use_os_module.setter
	def use_os_module(self,val : bool):
		self.var_use_os_module.set(val)

	@property
	def use_links(self) -> bool:
		return self.var_use_links.get()

	@use_links.setter
	def use_links(self, val: bool):
		self.var_use_links.set(val)
		
	@property
	def cleanup_debug_symbols(self) -> bool:
		return self.var_cleanup_debug_symbols.get()

	@cleanup_debug_symbols.setter
	def cleanup_debug_symbols(self,val : bool):
		self.var_cleanup_debug_symbols.set(val)

	@property
	def replace_main(self) -> bool:
		return self.var_replace_main.get()

	@replace_main.setter
	def replace_main(self,val : bool):
		self.var_replace_main.set(val)

	@property
	def cproject_path(self) -> str:
		return self.var_cproject_path.get() + "/.cproject"

	@property
	def project_path(self) -> str:
		return self.var_cproject_path.get() + "/.project"


	@cproject_path.setter
	def cproject_path(self, val: str):
		self.var_cproject_path.set(val)
	
	@property
	def sool_destination_path(self) -> str:
		return self.var_sool_destination_path.get()

	@sool_destination_path.setter
	def sool_destination_path(self, val: str):
		self.var_sool_destination_path.set(val)
		
	@property
	def sool_path(self) -> str:
		return self.var_sool_path.get()

	@sool_path.setter
	def sool_path(self, val: str):
		self.var_sool_path.set(val)
		
	@property
	def sool_chip(self) -> str:
		return self.var_sool_chip.get()

	@sool_chip.setter
	def sool_chip(self, val: str):
		self.var_sool_chip.set(val)