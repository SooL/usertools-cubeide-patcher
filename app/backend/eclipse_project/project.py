import typing as T
import xml.etree.ElementTree as ET
import os

from .ressource import ProjectRessource

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
		self.root : ET.Element = None
		self.ressources :T.Dict[str,ProjectRessource] = dict()
		self.name = None

	def load(self, path):
		with open(path,"r") as xml_file:
			self.root = ET.fromstring(xml_file.read())
			self.name = self.root.find("name").text

			natures : T.List[str] = list()
			for n in self.root.findall("natures/nature") :
				natures.append(n.text.split(".")[-1])

			if "cnature" not in natures :
				raise MissingCNatureException()
			if "ccnature" not in natures :
				raise MissingCPPNatureException()
			if "MCUProjectNature" not in natures :
				raise MissingMCUNatureException()

			for ressource in self.root.findall("linkedResources/link") :
				rsc = ProjectRessource.from_xml(ressource)
				self.ressources[rsc.project_path] = rsc

	def save_ressources(self):
		linked_section = self.root.find("linkedResources")

		for link in list(linked_section) :
			linked_section.remove(link)
		for link in self.ressources.values() :
			linked_section.append(link.to_xml())

	def save(self, output_file_path):
		self.save_ressources()
		with open(output_file_path, "wb") as out:
			data = ET.tostring(self.root, encoding="utf-8", xml_declaration=True)
			out.write(data)

	def add_resource(self, resource : ProjectRessource):
		self.ressources[resource.project_path] = resource