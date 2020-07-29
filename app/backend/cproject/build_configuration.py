import xml.etree.ElementTree as ET
import typing as T

class MissingDefineSectionError(RuntimeError):
	def __init__(self,*args):
		super().__init__(args)


class MissingIncludeSectionError(RuntimeError):
	def __init__(self,*args):
		super().__init__(args)

class CProjectConfiguration :

	@staticmethod
	def __extract_listValues_node(node) -> T.List[str]:
		ret = list()
		for value in node.findall("listOptionValue"):
			ret.append(value.attrib["value"])

		return ret

	def __init__(self,root : ET.Element):

		self.cppdefines_node : ET.Element = None
		self.cdefines_node: ET.Element = None

		self.cppdefines : T.List[str]= set()
		self.cdefines : T.List[str]= set()

		self.cpcincludes_node : ET.Element = None
		self.cincludes_node: ET.Element = None

		self.cpcincludes : T.List[str]= set()
		self.cincludes : T.List[str]= set()

		self.name : str = None

		self.root : ET.Element = None
		self.load_xml(root)


	def load_xml(self,root : ET.Element):
		self.root = root
		self.name = root.attrib["id"].split(".")[-2]

		for tool in self.root.findall("storageModule/configuration/folderInfo/toolChain/tool") :
			if tool.attrib["id"].split('.')[-3:-1] == ["c","compiler"] :
				self.cdefines_node = self.__get_define_node(tool)
				self.cdefines = self.__extract_listValues_node(self.cdefines_node)

				self.cincludes_node = self.__get_include_node(tool)
				self.cincludes = self.__extract_listValues_node(self.cincludes_node)
			elif tool.attrib["id"].split('.')[-3:-1] == ["cpp","compiler"] :
				self.cppdefines_node = self.__get_define_node(tool)
				self.cppdefines = self.__extract_listValues_node(self.cppdefines_node)

				self.cppincludes_node = self.__get_include_node(tool)
				self.cppincludes = self.__extract_listValues_node(self.cppincludes_node)

	def __get_define_node(self,tool) -> ET.Element:
		for option in tool.findall("option"):
			if option.attrib["id"].split(".")[-2] == "definedsymbols":
				return option
		raise MissingDefineSectionError

	def __get_include_node(self,tool) -> ET.Element:
		for option in tool.findall("option"):
			if option.attrib["id"].split(".")[-2] == "includepaths":
				return option
		raise MissingIncludeSectionError

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

	def clear_includes(self):
		self.cppincludes.clear()
		self.cincludes.clear()

	def add_include(self, param):
		self.add_cinclude(param)
		self.add_cppinclude(param)


	def add_cppinclude(self, param):
		self.cppincludes.append(param)

	def add_cinclude(self, param):
		self.cincludes.append(param)

	def save_includes(self):
		for elt in list(self.cincludes_node):
			self.cincludes_node.remove(elt)
		for elt in list(self.cppincludes_node):
			self.cppincludes_node.remove(elt)

		for include in self.cincludes:
			ET.SubElement(self.cincludes_node, "listOptionValue", {"builtInt": "false", "value": include})

		for include in self.cppincludes:
			ET.SubElement(self.cppincludes_node, "listOptionValue", {"builtInt": "false", "value": include})


