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

	def handle_sool_defines(self):
		print("Editing defines...")
		if self.params.cleanup_debug_symbols :
			print(f"\tSet chip to {self.params.sool_chip}")
			self.cproject_file.cleanup_defines()
			self.cproject_file.add_define(self.params.sool_chip)
		else :
			print("\tSkipped")

	def add_modules_defines(self):
		print("Adding modules defines...")
		for module in self.params.modules_selected_list :
			for define,val in module.defines.items() :
				self.cproject_file.add_define(define,val)

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

	def handle_modules(self):
		print("Adding some spicy modules...")
		for module in self.params.modules_selected_list :
			module_root = f"{self.params.project_sool_dir}/{self.params.modules_destination_path}"
			module_dest = f"{module_root}/{module.dirname}"

			if self.params.use_links :
				print(f"\tAdd {module.name} to project ressources")
				mod_ressource = ProjectRessource(module.root_path, module_dest)
				if not mod_ressource.type == ProjectRessource.FOLDER:
					raise RuntimeError()
				self.project_file.add_resource(mod_ressource)
			else :
				if not os.path.exists(module_root):
					print("\tCreating destination Module root directory")
					os.makedirs(module_root)

				if os.path.exists(module_dest):
					print("\tOverwriting module...")
					shutil.rmtree(module_dest)

				print(f"\tCopying {module.name} into {module_dest}")
				shutil.copytree(module.root_path,module_dest,dirs_exist_ok=True)


	def handle_sool_includes_paths(self):
		print("Rebuilding include tree...")
		print("\tAdding include paths")
		pattern = '"${{workspace_loc:/${{ProjName}}/{Base:s}/{SubPath:s}}}"'
		self.cproject_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core"))
		self.cproject_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core/include"))
		self.cproject_file.add_include(pattern.format(Base=self.params.sool_destination_path, SubPath="core/system/include"))

	def handle_modules_includes_paths(self):
		print("\tAdding modules include paths")
		pattern = '"${{workspace_loc:/${{ProjName}}/{Base:s}/{Module:s}/{SubPath:s}}}"'
		base_rep = f"{self.params.sool_destination_path}/{self.params.modules_destination_path}"
		for module in self.params.modules_selected_list :
			for inc in module.include_paths :
				self.cproject_file.add_include(pattern.format(Base=base_rep,Module=module.dirname, SubPath=inc))

	def handle_sool_source_paths(self):
		print("Adding SooL to source tree...")
		print("\tAdding source paths")
		self.cproject_file.add_source_path(f"{self.params.sool_destination_path}",not self.params.use_links)

	def run(self):
		print("Starting run...")
		self.params.print()
		self.init()
		self.handle_sool_defines()
		self.handle_sool()
		self.handle_sool_includes_paths()
		self.handle_sool_source_paths()

		if len(self.params.modules_selected_list) > 0 :
			self.handle_modules()
			self.handle_modules_includes_paths()
			self.add_modules_defines()

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
