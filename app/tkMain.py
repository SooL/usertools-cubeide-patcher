from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox


from .backend import Parameters
from .backend import Patcher
from .backend.module_manifest import ModuleManifest
from .tk_browse_field import BrowseField
from .tk_labeled_input import LabeledInput

from .backend.sool import SoolManifest

import os
import typing as T

class MainUI(Frame) :
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.params = Parameters(self)
		self.manifest_handler = SoolManifest()
		self.build_ui()
		self.sync_fields()

		self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.on_close)


	def build_ui(self):
		self.project_root = StringVar(self)
		project_frame = LabelFrame(self,text="Project parameters")
		project_root = BrowseField("Project folder : ",self.params.var_cproject_path,self.browse_CProjectFile,project_frame)
		project_sool_path = LabeledInput("SooL destination : ", self.params.var_sool_destination_path,project_frame)
		cleanup_debug_symbols_checkbox = Checkbutton(project_frame, text="Perform cleanup on debug symbols",variable=self.params.var_cleanup_debug_symbols)
		use_links_checkbox = Checkbutton(project_frame, text="Use links instead of hardcopy", variable=self.params.var_use_links)
		replace_main_checkbox = Checkbutton(project_frame, text="Replace \"main.c\" by a demo file \"main.cpp\"", variable=self.params.var_replace_main)

		sool_frame = LabelFrame(self,text="SooL parameters")
		sool_root = BrowseField("Sool Root : ",self.params.var_sool_path,self.browse_sool,sool_frame, on_edit=self.on_sool_path_change)

		self.sool_chip_treeview = Treeview(sool_frame,selectmode="browse",height=5)
		self.sool_chip_treeview.heading("#0", text="SooL Chip Define")
		self.sool_chip_treeview.bind("<ButtonRelease-1>",self.on_chip_select)

		sool_selected_chip = LabeledInput("Chip : ",self.params.var_sool_chip,sool_frame)

		# Modules definitions
		module_frame = LabelFrame(self,text="Modules")
		label_module = Label(module_frame,text="Available modules")
		self.modules_lists = Listbox(module_frame,selectmode="multiple")
		self.add_module_button = Button(module_frame,text="Register a new module",command=self.register_module)

		run = Button(self,text="Put some SooL into my project !",command=self.on_run)
		# Project packing
		project_root.pack(expand=TRUE,fill=X,side=TOP)
		project_sool_path.pack(expand=TRUE,fill=X,side=TOP)
		cleanup_debug_symbols_checkbox.pack(expand=TRUE,fill=X, side=TOP)
		use_links_checkbox.pack(expand=TRUE,fill=X, side=TOP)
		replace_main_checkbox.pack(expand=TRUE, fill=X, side=TOP)

		#Sool Packing
		sool_root.pack(fill=X,side=TOP)
		self.sool_chip_treeview.pack(fill=BOTH,side=TOP,expand=TRUE)
		sool_selected_chip.pack(fill=X,side=TOP)
		# generate_unified_includes_checkbox.pack(fill=X,side=TOP)

		#Module Packing
		label_module.pack(fill=X,side=TOP)
		self.modules_lists.pack(fill=X,side=TOP)
		self.add_module_button.pack(fill=X,side=TOP)

		project_frame.grid(row=0,sticky="new")
		sool_frame.grid(row=1,sticky="nsew")
		module_frame.grid(row=2,sticky="new")

		run.grid(row=3,sticky="sew",pady=(5,0))

		self.rowconfigure(1, weight=1)
		for col_num in range(self.grid_size()[0]):
			self.columnconfigure(col_num, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.master.rowconfigure(0, weight=1)

		self.grid(sticky="nsew",padx=5,pady=5)

		self.update_modules_list()


	def register_module(self, thinggy=None):
		path = filedialog.askopenfilename(title="Select the manifest for your module",
										  filetypes=(("Project file", "manifest.xml"), ("XML file","*.xml"),("All files", "*.*")))
		if os.path.exists(path) :
			new_mod = ModuleManifest(path)
			new_mod.read()
			self.params.modules_list.append(new_mod)
			self.update_modules_list()

	def update_modules_list(self):
		selected_index = self.modules_lists.curselection()
		selected_modules_names = [self.modules_lists.get(0,'end')[x] for x in selected_index]
		self.params.modules_list = sorted(self.params.modules_list,key=lambda x : x.name)
		still_valid_selected = set(selected_modules_names) & set([x.name for x in self.params.modules_list])
		new_list = sorted([x.name for x in self.params.modules_list])
		self.modules_lists.selection_clear(0,'end')
		self.modules_lists.delete(0,'end')
		for e in new_list :
			self.modules_lists.insert('end',e)
		indexes = [new_list.index(x) for x in list(still_valid_selected)]
		for i in indexes :
			self.modules_lists.selection_set(i)



	def sync_fields(self):
		if self.params.sool_path != "" :
			self.load_manifest(f"{self.params.sool_path}/manifest.xml")

	def browse_CProjectFile(self,thinggy=None):
		path = filedialog.askopenfilename(title="Select the CProject file for your project", filetypes=(("Project file",".cproject"),("All files","*.*")))
		path = os.path.dirname(path)
		#path = filedialog.askdirectory()
		if len(path) and os.path.exists(path) :
			if not os.path.exists(f"{path}/.cproject") :
				messagebox.showerror("CProject not found","The .cproject file was not found in the given filder.\n"
														  "Are you sure this is a proper STM32 Project ?")
			else :
				self.params.cproject_path = f"{path}"

	def browse_sool(self,thinggy=None):
		path = filedialog.askopenfilename(title="Select the manifest of the sool distrib",
										  filetypes=(("Manifest", "manifest.xml"), ("All files", "*.*")))
		path = os.path.dirname(path)
		if len(path) and os.path.exists(path) :
			self.params.sool_path = path

	def on_sool_path_change(self,new_path):
		if self.params.sool_module_path == "" :
			self.params.sool_module_path = os.path.normpath(self.params.sool_path + "/modules")

		self.load_manifest(f"{self.params.sool_path}/manifest.xml")

	def browse_modules(self, thinggy=None):
		path = filedialog.askdirectory()
		if len(path) and os.path.exists(path):
			self.params.sool_module_path = path

	def load_manifest(self,path : str):
		if os.path.exists(path) :
			self.manifest_handler.read(path)
			self.load_chips(self.manifest_handler.chips)

	def load_chips(self,stm_dictionary : T.Dict[str,T.List[str]]) :
		if len(self.sool_chip_treeview.get_children()) > 0 :
			for iid in self.sool_chip_treeview.get_children() :
				self.sool_chip_treeview.delete(iid)
		for family in sorted(stm_dictionary.keys()) :
			fam_iid = self.sool_chip_treeview.insert("","end",text=family)
			for chip in sorted(stm_dictionary[family]) :
				self.sool_chip_treeview.insert(fam_iid,"end",text=chip)

	def on_close(self, *args):
		self.params.write_parameters()
		self.master.destroy()

	def on_chip_select(self,event):
		if len(self.sool_chip_treeview.selection()) > 0 :
			chipname = self.sool_chip_treeview.item(self.sool_chip_treeview.selection()[0])["text"]
			if len(chipname) > 8 :
				self.params.sool_chip = chipname

	def on_run(self,thinggy=None):
		patcher = Patcher(self.params)
		try:
			patcher.run()
		except Exception as e :
			messagebox.showerror("Error","An unexpected error occured while patching:\n"
								 f"Error {e.__cause__}")
			raise e
		else:
			messagebox.showinfo("SooL Patcher","Patching done !")
