import typing as T
import xml.etree.ElementTree as ET
import os

class ProjectRessource:
	FILE = 1
	FOLDER = 2

	def __init__(self, filesystem_location, project_path=None, rsc_type = None):
		self.location = filesystem_location
		self.project_path = project_path if project_path is not None else os.path.basename(filesystem_location)
		self.is_absolute_path = True
		if rsc_type is not None and rsc_type in (self.FILE,self.FOLDER) :
			self.type = rsc_type
		else :
			self.type = self.FILE if os.path.isfile(self.location) else self.FOLDER

	@classmethod
	def from_xml(cls, root : ET.Element):
		if not root.tag == "link" :
			raise RuntimeError(f"Invalid type of root element {root.tag}")
		project_loc = root.find("name").text
		rsc_type = int(root.find("type").text)
		location_path = None
		is_absolute = True
		loc = root.find("location")
		if loc is not None :
			location_path = loc.text
			# Is absolute path

		if location_path is None :
			loc = root.find("locationURI")
			# Is relative path
			if loc is not None :
				location_path = loc.text
				is_absolute = False

		ret = cls(location_path,project_loc,rsc_type)
		ret.is_absolute_path = is_absolute
		return ret

	def to_xml(self) -> ET.Element:
		root = ET.Element("link")
		n = ET.SubElement(root,"name")
		n.text = self.project_path

		t = ET.SubElement(root,"type")
		t.text=str(self.type)

		l = ET.SubElement(root,"location" if self.is_absolute_path else "locationURI")
		l.text=self.location

		return root


