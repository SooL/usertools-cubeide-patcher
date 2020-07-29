import unittest as ut
import xml.etree.ElementTree as ET
from .cproject import CProject, CProjectConfiguration
from .cproject import InvalidCProjectFileError, NoCConfigurationError, MissingDefineSectionError
import os


class CProjectTestCase(ut.TestCase):
	def setUp(self):
		self.cproject = CProject()
		self.tc_valid = f"{os.path.dirname(__file__)}/testcases/valid.cproject"
		self.tc_invalid_cconf= f"{os.path.dirname(__file__)}/testcases/invalid/nocconf.cproject"
		self.tc_invalid_root = f"{os.path.dirname(__file__)}/testcases/invalid/root.cproject"

		# Debug has empty define section and release doesn't have any define section
		self.tc_nodefines = f"{os.path.dirname(__file__)}/testcases/invalid/nodefinesections.cproject"

		# Valid define section but empty
		self.tc_emptydefines = f"{os.path.dirname(__file__)}/testcases/invalid/empty_cpp_defines.cproject"

		self.output_tc = f"{os.path.dirname(__file__)}/testcases/out.xml"
		if os.path.exists(self.output_tc) :
			os.remove(self.output_tc)


	def test_load(self):
		self.cproject.load(self.tc_valid)

	def test_is_valid_file(self):
		self.cproject.load(self.tc_valid)
		self.assertTrue(self.cproject.isvalid)
		self.assertTrue(isinstance(self.cproject.root, ET.Element))

	def test_is_invalid_at_start(self):
		self.assertFalse(self.cproject.isvalid)

	def test_raise_unknown_file(self):
		with self.assertRaises(FileNotFoundError) :
			self.cproject.load("innexistant_thinggy")

	def test_invalid_on_unkown_file(self):
		try:
			self.cproject.load("unknown")
		except FileNotFoundError :
			pass
		self.assertFalse(self.cproject.isvalid)

	def test_invalid_root(self):
		with self.assertRaises(InvalidCProjectFileError):
			self.cproject.load(self.tc_invalid_root)

	def test_invalid_on_invalid_root(self):
		try:
			self.cproject.load(self.tc_invalid_root)
		except InvalidCProjectFileError:
			pass
		self.assertFalse(self.cproject.isvalid)

	def test_load_without_cconf(self):
		with self.assertRaises(NoCConfigurationError) :
			self.cproject.load(self.tc_invalid_cconf)

	def test_invalid_on_load_without_cconf(self):
		try :
			self.cproject.load(self.tc_invalid_cconf)
		except NoCConfigurationError:
			pass
		self.assertFalse(self.cproject.isvalid)

	def test_get_configurations(self):
		self.cproject.load(self.tc_valid)

		self.assertTrue(isinstance(self.cproject.configurations,list))
		self.assertEqual(len(self.cproject.configurations),2)

		for configuration in self.cproject :
			self.assertTrue(isinstance(configuration,CProjectConfiguration))

		self.assertTrue(isinstance("thing" in self.cproject,bool))
		self.assertTrue("release" in self.cproject)
		self.assertTrue("debug" in self.cproject)

	def test_get_configuration_defines(self):
		self.cproject.load(self.tc_valid)
		self.assertTrue(self.cproject.isvalid)
		self.assertEqual(self.cproject["release"].cdefines, ["STM32", "STM32F303K8Tx", "STM32F3"])
		self.assertEqual(self.cproject["debug"].cdefines, ["STM32", "STM32F303K8Tx", "STM32F3", "DEBUG"])

		self.assertEqual(self.cproject["release"].cppdefines, ["STM32", "STM32F303K8Tx", "STM32F3"])
		self.assertEqual(self.cproject["debug"].cppdefines, ["STM32", "STM32F303K8Tx", "STM32F3", "DEBUG"])

	def test_no_defines_section(self):
		with self.assertRaises(MissingDefineSectionError) :
			self.cproject.load(self.tc_nodefines)

	def test_invalid_on_no_define_section(self):
		try :
			self.cproject.load(self.tc_nodefines)
		except MissingDefineSectionError:
			pass

		self.assertFalse(self.cproject.isvalid)

	def test_empty_defines_section(self):
		self.cproject.load(self.tc_emptydefines)
		self.assertTrue(self.cproject.isvalid)
		self.assertEqual(self.cproject["release"].cppdefines, [])
		self.assertEqual(self.cproject["debug"].cppdefines, [])

	def test_cleanup_defines(self):
		self.cproject.load(self.tc_valid)
		self.cproject.cleanup_defines()

		self.assertEqual(self.cproject["release"].cppdefines, [])
		self.assertEqual(self.cproject["debug"].cppdefines, ["DEBUG"])

	def test_output_xml(self):
		self.cproject.load(self.tc_valid)
		self.cproject.save(self.output_tc)
		reload = CProject()
		reload.load(self.output_tc)
		self.assertTrue(reload.isvalid)


	def test_saved_defines(self):
		self.cproject.load(self.tc_valid)
		self.cproject.cleanup_defines()
		self.cproject.save(self.output_tc)

		reload = CProject()
		reload.load(self.output_tc)

		self.assertEqual([],       reload["release"].cppdefines)
		self.assertEqual(["DEBUG"],reload["debug"].cppdefines)

		self.assertEqual([],       reload["release"].cdefines)
		self.assertEqual(["DEBUG"],reload["debug"].cdefines)

	def test_add_define(self):
		self.cproject.load(self.tc_valid)
		self.cproject.cleanup_defines()
		self.cproject["debug"].add_define("_D1")

		self.assertEqual(["DEBUG","_D1"], self.cproject["debug"].cppdefines)
		self.assertEqual(["DEBUG","_D1"], self.cproject["debug"].cdefines)

		self.cproject["debug"].add_cdefine("_D2")
		self.cproject["debug"].add_cppdefine("_D3")
		self.assertEqual(["DEBUG","_D1","_D3"], self.cproject["debug"].cppdefines)
		self.assertEqual(["DEBUG","_D1","_D2"], self.cproject["debug"].cdefines)

		self.assertEqual([],self.cproject["release"].cdefines)
		self.assertEqual([],self.cproject["release"].cppdefines)

	def test_save_added_defines(self):
		self.cproject.load(self.tc_valid)
		self.cproject.cleanup_defines()

		self.cproject["debug"].add_define("_D1")
		self.cproject["debug"].add_cdefine("_D2")
		self.cproject["debug"].add_cppdefine("_D3")

		self.cproject.save(self.output_tc)

		reload = CProject()
		reload.load(self.output_tc)

		self.assertEqual(["DEBUG", "_D1", "_D3"], reload["debug"].cppdefines)
		self.assertEqual(["DEBUG", "_D1", "_D2"], reload["debug"].cdefines)

		self.assertEqual([], reload["release"].cdefines)
		self.assertEqual([], reload["release"].cppdefines)

