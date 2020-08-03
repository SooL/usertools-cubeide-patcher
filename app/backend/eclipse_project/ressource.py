import typing as T
import xml.etree.ElementTree as ET
import os

class ProjectRessource:
	FILE = 1
	FOLDER = 2

	def __init__(self, filesystem_location, project_path=None, rsc_type = None):
		self.location = filesystem_location
		self.project_path = project_path if project_path is not None else os.path.basename(filesystem_location)

		if rsc_type is not None and rsc_type in (self.FILE,self.FOLDER) :
			self.type = rsc_type
		else :
			self.type = self.FILE if os.path.isfile(self.location) else self.FOLDER

	@classmethod
	def from_xml(cls, root : ET.Element):
		if not root.tag == "link" :
			raise RuntimeError("Invalid type of root element")
		project_loc = root.find("name").text
		rsc_type = int(root.find("type").text)
		location = root.find("locationURI").text

		return cls(location,project_loc,rsc_type)

	def to_xml(self) -> ET.Element:
		root = ET.Element("link")
		n = ET.SubElement(root,"name")
		n.text = self.project_path

		t = ET.SubElement(root,"type")
		t.text=str(self.type)

		l = ET.SubElement(root,"locationURI")
		l.text=self.location

		return root


