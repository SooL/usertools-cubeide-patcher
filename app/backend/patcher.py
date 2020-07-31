from .ParametersHandler import Parameters
from .cproject import CProject
import shutil
import os



class Patcher():
	def __init__(self, params : Parameters):
		self.params : Parameters = params
		self.project_file = CProject()


	def init(self) :
		print(f"{'':=<80s}")
		print("Initialization step...")
		print("\tCreating backup")
		shutil.copy2(self.params.cproject_path, f"{self.params.cproject_path}.bak")
		print("\tLoading CProject file")
		self.project_file.load(self.params.cproject_path)

	def handle_defines(self):
		print("Editing defines...")
		if self.params.cleanup_debug_symbols :
			print(f"\tSet chip to {self.params.sool_chip}")
			self.project_file.cleanup_defines()
			self.project_file.add_define(self.params.sool_chip)
		else :
			print("\tSkipped")

	def handle_sool(self):
		print("Moving SooL around...")
		if not os.path.exists(os.path.dirname(self.params.project_sool_dir)) :
			print("\tCreating destination SooL parent directory")
			os.makedirs(os.path.dirname(self.params.project_sool_dir))
		if not os.path.exists(self.params.project_sool_dir) :
			print(f"\tCopying sool into {self.params.project_sool_dir}")
			shutil.copytree(self.params.sool_path,self.params.project_sool_dir)
		else:
			raise FileExistsError()

	def handle_includes_paths(self):
		print("Rebuilding include tree...")
		print("\tAdding include paths")
		pattern = '"${{workspace_loc:/${{ProjName}}/{Base:s}/{SubPath:s}}}"'
		self.project_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core"))
		self.project_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core/include"))
		self.project_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core/system/include"))

	def handle_source_paths(self):
		print("Adding SooL to source tree...")
		print("\tAdding source paths")
		self.project_file.add_source_path(f"{self.params.sool_destination_path}")

	def run(self):
		print("Starting run...")
		self.params.print()
		self.init()
		self.handle_defines()
		self.handle_sool()
		self.handle_includes_paths()
		self.handle_source_paths()

		print("Writing destination file...")
		self.project_file.save(self.params.cproject_path)

