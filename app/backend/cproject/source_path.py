import xml.etree.ElementTree as ET

class SourcePath :
	def __init__(self, path : str, resolved = True):
		self.path : str = path
		self.resolved : bool = resolved
		self.is_workspace_path = True

	@classmethod
	def from_xml(cls,elt :ET.Element):
		if elt.tag != "entry" :
			raise RuntimeError(f"Invalid tag {elt.tag}, expected 'entry'")
		path = elt.attrib["name"]
		flaglist = elt.attrib["flags"].split("|")

		resolved = "RESOLVED" in flaglist
		return cls(path,resolved)

	def to_xml(self):
		return ET.Element("entry",flags=self.flag_string, kind="sourcePath", name=self.path)

	@property
	def flag_string(self):
		flist = list()
		if self.is_workspace_path :
			flist.append("VALUE_WORKSPACE_PATH")
		if self.resolved :
			flist.append("RESOLVED")
		return "|".join(flist)

	def __eq__(self, other):
		if isinstance(other,str) :
			return self.path == other
		if isinstance(other,SourcePath) :
			return self.path == other.path and \
				   self.resolved == other.resolved
