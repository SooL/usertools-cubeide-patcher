
from .build_configuration import CProjectConfiguration
from .build_configuration import MissingDefineSectionError
import os
import typing as T
import xml.etree.ElementTree as ET


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

	def load(self, filepath):
		with open(filepath,"r") as xml_file :
			self.root = ET.fromstring(xml_file.read())
			if self.root.tag != "cproject" :
				raise InvalidCProjectFileError()

			failed_to_load_valid_conf = False
			for configuration_xml in self.root.findall("storageModule/cconfiguration") :
				try :
					configuration = CProjectConfiguration(configuration_xml)
				except MissingDefineSectionError :
					failed_to_load_valid_conf = True
				else:
					self.configurations.append(configuration)

			if len(self) == 0 :
				if failed_to_load_valid_conf :
					raise  MissingDefineSectionError()
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

	def save(self, output_file_path):
		for configuration in self :
			configuration.save_defines()
			pass

		with open(output_file_path,"wb") as out :
			data = bytes('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',encoding="utf-8")
			data += ET.tostring(self.root,encoding="utf-8",xml_declaration=False)
			out.write(data)

	


