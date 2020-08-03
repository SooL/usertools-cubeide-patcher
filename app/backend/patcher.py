from .ParametersHandler import Parameters
from .cproject import CProject
from .eclipse_project import Project, ProjectRessource
import shutil
import os

main_content = """
#include <sool_setup.h>
#include <GPIO.h>

int main(void)
{
	using namespace sool::core;
	GPIOA->enable_clock();

	PA3 = GPIO::Mode::Output | GPIO::OutType::PushPull;

	for(;;)
	{
		for(int i = 0; i < 50000; i++)
			asm("nop");
		PA3.toggle();
	}
}
"""

class Patcher():
	def __init__(self, params : Parameters):
		self.params : Parameters = params
		self.cproject_file = CProject()
		self.project_file = Project()


	def init(self) :
		print(f"{'':=<80s}")
		print("Initialization step...")
		print("\tCreating backup")
		shutil.copy2(self.params.cproject_path, f"{self.params.cproject_path}.bak")
		shutil.copy2(self.params.project_path, f"{self.params.project_path}.bak")
		print("\tLoading CProject file")
		self.cproject_file.load(f"{self.params.cproject_path}")
		print("\tLoading Project file")
		self.project_file.load(f"{self.params.project_path}")

	def handle_defines(self):
		print("Editing defines...")
		if self.params.cleanup_debug_symbols :
			print(f"\tSet chip to {self.params.sool_chip}")
			self.cproject_file.cleanup_defines()
			self.cproject_file.add_define(self.params.sool_chip)
		else :
			print("\tSkipped")

	def handle_sool(self):

		print("Moving SooL around...")
		if self.params.use_links :
			print("\tAdd sool to project resources")
			sool_resource = ProjectRessource(self.params.sool_path,self.params.sool_destination_path)
			if not sool_resource.type == ProjectRessource.FOLDER :
				raise RuntimeError()
			self.project_file.add_resource(sool_resource)
		else :
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
		self.cproject_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core"))
		self.cproject_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core/include"))
		self.cproject_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core/system/include"))

	def handle_source_paths(self):
		print("Adding SooL to source tree...")
		print("\tAdding source paths")
		self.cproject_file.add_source_path(f"{self.params.sool_destination_path}",not self.params.use_links)

	def run(self):
		print("Starting run...")
		self.params.print()
		self.init()
		self.handle_defines()
		self.handle_sool()
		self.handle_includes_paths()
		self.handle_source_paths()

		print("Writing destination file...")
		self.cproject_file.save(self.params.cproject_path)
		self.project_file.save(self.params.project_path)

		print("Finalizing...")
		self.finalize_fileset()
		print("Done !")

	def finalize_fileset(self):
		if self.params.replace_main :
			print("\tReplace main.c...")
			if os.path.exists(f"{self.params.project_dir}/Src/main.c") :
				os.remove(f"{self.params.project_dir}/Src/main.c")
				with open(f"{self.params.project_dir}/Src/main.cpp","w") as main_file :
					main_file.write(main_content)
