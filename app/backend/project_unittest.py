import unittest as ut
import xml.etree.ElementTree as ET

from .eclipse_project import Project
from .eclipse_project import InvalidNatureException
from .eclipse_project import MissingCNatureException
from .eclipse_project import MissingCPPNatureException
from .eclipse_project import MissingMCUNatureException

from .eclipse_project import ProjectRessource

import os


class ProjectTestCase(ut.TestCase):
	def setUp(self):
		self.project = Project()
		self.tc_valid = f"{os.path.dirname(__file__)}/testcases/valid.project"

		self.tc_no_c_nature = f"{os.path.dirname(__file__)}/testcases/invalid/noc.project"
		self.tc_no_cpp_nature = f"{os.path.dirname(__file__)}/testcases/invalid/nocpp.project"
		self.tc_no_mcu_nature = f"{os.path.dirname(__file__)}/testcases/invalid/nomcu.project"


		self.output_tc = f"{os.path.dirname(__file__)}/testcases/out.project"
		if os.path.exists(self.output_tc) :
			os.remove(self.output_tc)

	def tearDown(self) -> None:
		if os.path.exists(self.output_tc) :
			os.remove(self.output_tc)


	def test_load(self):
		self.project.load(self.tc_valid)

	def test_name(self):
		self.project.load(self.tc_valid)
		self.assertEqual("PatcheurF3",self.project.name)

	def test_check_nature(self):
		with self.assertRaises(MissingCNatureException) :
			self.project.load(self.tc_no_c_nature)
		with self.assertRaises(MissingCPPNatureException) :
			self.project.load(self.tc_no_cpp_nature)
		with self.assertRaises(MissingMCUNatureException) :
			self.project.load(self.tc_no_mcu_nature)

	def test_ressource(self):
		r = ProjectRessource("./")
		r.project_path = "t"
		r.type = ProjectRessource.FILE
		r.type = ProjectRessource.FOLDER
		r.location = "/a/path"

	def test_ressource_immediate_file_declaration(self):
		r = ProjectRessource(self.tc_valid)
		self.assertEqual(self.tc_valid,r.location)
		self.assertEqual("valid.project", r.project_path)
		self.assertEqual(ProjectRessource.FILE, r.type)

	def test_ressource_immediate_folder_declaration(self):
		r = ProjectRessource(os.path.dirname(self.tc_valid))
		self.assertEqual(os.path.dirname(self.tc_valid),r.location)
		self.assertEqual("testcases", r.project_path)
		self.assertEqual(ProjectRessource.FOLDER, r.type)

	def test_ressource_immediate_file_full_declaration(self):
		r = ProjectRessource(self.tc_valid,"foo.bar")
		self.assertEqual(self.tc_valid,r.location)
		self.assertEqual("foo.bar", r.project_path)
		self.assertEqual(ProjectRessource.FILE, r.type)


	def test_ressource_immediate_folder_full_declaration(self):
		r = ProjectRessource(os.path.dirname(self.tc_valid),"foo")
		self.assertEqual(os.path.dirname(self.tc_valid),r.location)
		self.assertEqual("foo", r.project_path)
		self.assertEqual(ProjectRessource.FOLDER, r.type)

	def test_ressource_from_xml(self):
		root = ET.Element("link")
		name = ET.SubElement(root,"name")
		name.text = "test"

		t = ET.SubElement(root,"type")
		t.text = 2

		location = ET.SubElement(root,"locationURI")
		location.text = self.tc_valid

		ressource = ProjectRessource.from_xml(root)
		self.assertEqual(self.tc_valid,ressource.location)
		self.assertEqual(ProjectRessource.FOLDER,ressource.type)
		self.assertEqual("test",ressource.project_path)

	def test_to_xml(self):
		r = ProjectRessource(self.tc_valid, "foo.bar")
		root = r.to_xml()
		r2 = ProjectRessource.from_xml(root)

		self.assertEquals(r.location,r2.location)
		self.assertEquals(r.project_path,r2.project_path)
		self.assertEquals(r.type,r2.type)

