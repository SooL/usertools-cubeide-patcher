import unittest
from module_manifest import ModuleManifest
import os


class ModuleManifest_Test(unittest.TestCase):
	def setUp(self) -> None:
		self.valid_root = "testcases/module"
		self.valid_tc = f"{self.valid_root}/manifest.xml"
		self.valid_incdir = "testcases/module/include"
		self.valid_modmanif = ModuleManifest(self.valid_tc)

	def test_init(self):
		self.assertEqual(self.valid_tc,self.valid_modmanif.path)
		self.assertEqual(self.valid_root, self.valid_modmanif.root_path)
		self.assertEqual(0,len(self.valid_modmanif.include_paths))
		self.assertEqual(0,len(self.valid_modmanif.source_paths))

	def test_add_relative_incdir(self):
		self.valid_modmanif.add_incdir(self.valid_incdir)
		self.assertTrue(os.path.exists(f"{self.valid_root}/{list(self.valid_modmanif.include_paths)[0]}"))

	def test_add_abs_incdir(self):
		self.valid_modmanif.add_incdir(os.path.abspath(self.valid_incdir))
		self.assertTrue(os.path.exists(f"{self.valid_root}/{list(self.valid_modmanif.include_paths)[0]}"))

	def test_add_source(self):
		self.valid_modmanif.add_source("testcases/module/src/added.cpp")
		self.assertTrue(os.path.exists(f"{self.valid_root}/{list(self.valid_modmanif.source_paths)[0]}"))

	def test_read(self):
		self.valid_modmanif.read()
		self.assertIn("include",self.valid_modmanif.include_paths)
		self.assertIn("src",self.valid_modmanif.source_paths)

if __name__ == '__main__':
	unittest.main()
