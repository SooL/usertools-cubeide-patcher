
from .build_configuration import CProjectConfiguration
from .build_configuration import MissingDefineSectionError
from .build_configuration import MissingIncludeSectionError

import typing as T
import xml.etree.ElementTree as ET
import os

class InvalidCProjectFileError(RuntimeError):
	def __init__(self,*args):
		super().__init__(args)


class NoCConfigurationError(RuntimeError):
	def __init__(self,*args):
		super().__init__(args)

class CProject :
	def __init__(self):
		self.configurations = list()
		self.root : ET.Element = None
		self.isvalid = False

	def load(self, filepath : str):
		if not (os.path.exists(filepath) and not os.path.isdir(filepath)) :
			raise FileNotFoundError(f"{filepath} in valid .cproject file")
		with open(filepath,"r") as xml_file :
			self.root = ET.fromstring(xml_file.read())
			if self.root.tag != "cproject" :
				raise InvalidCProjectFileError()

			failed_to_load_section_error = None
			for configuration_xml in self.root.findall("storageModule/cconfiguration") :
				try :
					configuration = CProjectConfiguration(configuration_xml)
				except MissingDefineSectionError as e:
					failed_to_load_section_error = e
					break
				except MissingIncludeSectionError as e:
					failed_to_load_section_error = e
					break
				else:
					self.configurations.append(configuration)


			if len(self) == 0 :
				if failed_to_load_section_error is not None :
					raise  failed_to_load_section_error
				else :
					raise NoCConfigurationError()

			self.isvalid = True

		pass

	def __iter__(self) -> T.Iterable[CProjectConfiguration]:
		return self.configurations.__iter__()

	def __contains__(self, item) -> bool:
		c : CProjectConfiguration
		for c in self :
			if c.name == item :
				return True

	def __getitem__(self, item) -> CProjectConfiguration:
		for c in self :
			if c.name == item :
				return c

	def __len__(self):
		return len(self.configurations)

	def cleanup_defines(self):
		for configuration in self :
			configuration.cleanup_defines()
			pass

	def cleanup_includes(self):
		for configuration in self:
			configuration.clear_includes()

	def save(self, output_file_path):
		for configuration in self :
			configuration.save_defines()
			configuration.save_includes()
			configuration.save_sourcepaths()
			pass

		with open(output_file_path,"wb") as out :
			data = bytes('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<?fileVersion 4.0.0?>\n',encoding="utf-8")
			data += ET.tostring(self.root,encoding="utf-8",xml_declaration=False)
			out.write(data)

	def clear_paths(self):
		for configuration in self :
			configuration.clear_source_paths()

	def add_include(self, param):
		for configuration in self :
			configuration.add_include(param)

	def add_source_path(self, param, resolved = True):
		for configuration in self:
			configuration.add_source_path(param, resolved)

	def add_define(self, name, val = None):
		def_str = name
		if val is not None and len(str(val).strip()) > 0:
			def_str += f"={val}"
		for configuration in self:
			configuration.add_define(def_str)

	def add_cdefine(self, chip):
		for configuration in self:
			configuration.add_cdefine(chip)

	def add_cppdefine(self, chip):
		for configuration in self:
			configuration.add_cppdefine(chip)

	


