import xml.etree.ElementTree as ET
import typing as T

class MissingDefineSectionError(RuntimeError):
	def __init__(self,*args):
		super().__init__(args)


class CProjectConfiguration :

	@staticmethod
	def __extract_defines_from_node(node) -> T.List[str]:
		ret = list()
		for value in node.findall("listOptionValue"):
			ret.append(value.attrib["value"])

		return ret

	def __init__(self,root : ET.Element):

		self.cppdefines_node : ET.Element = None
		self.cdefines_node: ET.Element = None

		self.cppdefines : T.List[str]= set()
		self.cdefines : T.List[str]= set()
		self.name : str = None

		self.root : ET.Element = None
		self.load_xml(root)


	def load_xml(self,root : ET.Element):
		self.root = root
		self.name = root.attrib["id"].split(".")[-2]

		for tool in self.root.findall("storageModule/configuration/folderInfo/toolChain/tool") :
			if tool.attrib["id"].split('.')[-3:-1] == ["c","compiler"] :
				self.cdefines_node = self.__get_define_node(tool)
				self.cdefines = self.__extract_defines_from_node(self.cdefines_node)
			elif tool.attrib["id"].split('.')[-3:-1] == ["cpp","compiler"] :
				self.cppdefines_node = self.__get_define_node(tool)
				self.cppdefines = self.__extract_defines_from_node(self.cppdefines_node)

	def __get_define_node(self,tool) -> ET.Element:
		for option in tool.findall("option"):
			if option.attrib["id"].split(".")[-2] == "definedsymbols":
				return option
		raise MissingDefineSectionError


	def cleanup_defines(self):
		i = 0
		while i < len(self.cppdefines):
			if self.cppdefines[i].startswith("STM32"):
				self.cppdefines.pop(i)
			else:
				i += 1
		i = 0
		while i < len(self.cdefines):
			if self.cdefines[i].startswith("STM32"):
				self.cdefines.pop(i)
			else:
				i += 1

	def save_defines(self):
		for elt in list(self.cdefines_node) :
			self.cdefines_node.remove(elt)
		for elt in list(self.cppdefines_node) :
			self.cppdefines_node.remove(elt)

		for define in self.cdefines :
			ET.SubElement(self.cdefines_node,"listOptionValue",{"builtInt":"false","value":define})

		for define in self.cppdefines :
			ET.SubElement(self.cppdefines_node,"listOptionValue",{"builtInt":"false","value":define})

	def add_define(self, param):
		self.add_cdefine(param)
		self.add_cppdefine(param)


	def add_cppdefine(self, param):
		self.cppdefines.append(param)

	def add_cdefine(self, param):
		self.cdefines.append(param)


