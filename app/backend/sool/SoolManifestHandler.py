import xml.etree.ElementTree as ET
import typing as T
import os

class SoolManifest() :
	def __init__(self,path : str = None):
		if path is not None :
			self.read(path)
		else :
			self.root = None
		"""Family -> Chips"""
		self.chips : T.Dict[str,T.List[str]] = dict()

	def __read_chips(self):
		self.chips.clear()
		for family in self.root.findall("chips/family") :
			self.chips[family.attrib["name"]] = list()
			for chip in family.findall("chip") :
				self.chips[family.attrib["name"]].append(chip.attrib["define"])

	def contains_chip(self, chip : str) -> bool:
		"""
		Return true if the given chip is exactly registered as a define.
		:param chip: Chip string to test
		:return: True if the chip string is found.
		"""
		local_chip = chip.upper().replace("X","x")
		for family in self.chips :
			if local_chip.startswith(family) :
				for registered_chip in self.chips[family] :
					if local_chip == registered_chip :
						return True
		return False

	def chips_starting_with(self,pattern : str) -> T.Dict[str,T.List[str]] :
		local_chip = pattern.upper().replace("X","x")
		ret : T.Dict[str,T.List[str]] = dict()
		for family in self.chips :
			if family.startswith(local_chip) :
				ret[family] = list()
				for registered_chip in self.chips[family] :
					if registered_chip.startswith(registered_chip):
						ret[family].append(registered_chip)
		return ret

	@property
	def valid(self):
		return self.root is not None

	def read(self,path : str):
		with open(path, "r") as xml_file:
			self.root: ET.Element = ET.fromstring(xml_file.read())
			self.__read_chips()