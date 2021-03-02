import xml.etree.ElementTree as ET
import typing as T

import os

class ModuleManifest:
	def __init__(self, path : str):
		self.include_paths : T.Set[str] = set()
		self.source_paths : T.Set[str] = set()
		self.defines: T.Dict[str, str] = dict()

		self.path = path
		self.root_path = os.path.dirname(path)
		self.dirname = os.path.split(os.path.abspath(self.root_path))[-1]
		self.name = None

	def add_incdir(self, valid_incdir):
		p = self.get_relpath(valid_incdir)
		self.include_paths.add(p)

	def add_include(self, inc : str, val = ""):
		self.defines[inc] = val


	def get_relpath(self, path):
		p = os.path.abspath(path)
		p = os.path.relpath(p, os.path.abspath(self.root_path))
		return p

	def add_source(self, source):
		self.source_paths.add(self.get_relpath(source))
		pass

	def read(self):
		root = ET.parse(self.path).getroot()
		self.name = root.attrib["name"]
		for e in root.findall("inc") :
			path = e.attrib["path"]
			if os.path.exists(f"{self.root_path}/{path}") :
				self.include_paths.add(path)
		for e in root.findall("src") :
			path = e.attrib["path"]
			if os.path.exists(f"{self.root_path}/{path}") :
				self.source_paths.add(path)
		for e in root.findall("define") :
			define = e.attrib["name"]
			val = e.attrib["value"] if "value" in e.attrib else None
			self.add_include(define,val)
		pass