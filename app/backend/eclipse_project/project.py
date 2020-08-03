import typing as T
import xml.etree.ElementTree as ET
import os

class InvalidNatureException(Exception):
	def __init__(self,*args):
		super().__init__(args)

class MissingCNatureException(InvalidNatureException):
	def __init__(self,*args):
		super().__init__(args)

class MissingCPPNatureException(InvalidNatureException):
	def __init__(self,*args):
		super().__init__(args)

class MissingMCUNatureException(InvalidNatureException):
	def __init__(self, *args):
		super().__init__(args)

class Project:
	# Reference file format is at :
	# https://help.eclipse.org/2019-12/index.jsp?topic=%2Forg.eclipse.platform.doc.isv%2Freference%2Fmisc%2Fproject_description_file.html

	def __init__(self):
		self.name = "PatcheurF3"

	def load(self, path):
		with open(path,"r") as xml_file:
			root = ET.fromstring(xml_file.read())

			natures : T.List[str] = list()
			for n in root.findall("natures/nature") :
				natures.append(n.text.split(".")[-1])

			if "cnature" not in natures :
				raise MissingCNatureException()
			if "ccnature" not in natures :
				raise MissingCPPNatureException()
			if "MCUProjectNature" not in natures :
				raise MissingMCUNatureException()
		