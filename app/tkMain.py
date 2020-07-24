from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from .backend import Parameters

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
		project_root = BrowseField("CProject file : ",self.params.var_cproject_path,self.browse_CProjectFile,project_frame)
		project_sool_path = LabeledInput("SooL destination : ", self.params.var_sool_destination_path,project_frame)
		cleanup_debug_symbols_checkbox = Checkbutton(project_frame, text="Perform cleanup on debug symbols",variable=self.params.var_cleanup_debug_symbols)
		use_links_checkbox = Checkbutton(project_frame, text="Use links instead of hardcopy", variable=self.params.var_use_links)

		sool_frame = LabelFrame(self,text="SooL parameters")
		sool_root = BrowseField("Sool Root : ",self.params.var_sool_path,self.browse_sool,sool_frame, on_edit=self.on_sool_path_change)

		self.sool_chip_treeview = Treeview(sool_frame,selectmode="browse",height=5)
		self.sool_chip_treeview.heading("#0", text="SooL Chip Define")

		module_frame = LabelFrame(self,text="Modules parameters")
		sool_module = BrowseField("Modules Root : ", self.params.var_sool_module_path, self.browse_modules, module_frame)
		use_io_module_checkbox = Checkbutton(module_frame,text="Use IO module",variable=self.params.var_use_io_module)
		use_os_module_checkbox = Checkbutton(module_frame, text="Use OS module", variable=self.params.var_use_os_module)

		run = Button(self,text="Put some SooL into my project !")
		# Project packing
		project_root.pack(expand=TRUE,fill=X,side=TOP)
		project_sool_path.pack(expand=TRUE,fill=X,side=TOP)
		cleanup_debug_symbols_checkbox.pack(expand=TRUE,fill=X, side=TOP)
		use_links_checkbox.pack(expand=TRUE,fill=X, side=TOP)

		#Sool Packing
		sool_root.pack(fill=X,side=TOP)
		self.sool_chip_treeview.pack(fill=BOTH,side=TOP,expand=TRUE)
		# generate_unified_includes_checkbox.pack(fill=X,side=TOP)

		#Module Packing
		sool_module.pack(fill=X, side=TOP)
		use_io_module_checkbox.pack(fill=X,side=TOP)
		use_os_module_checkbox.pack(fill=X,side=TOP)

		project_frame.grid(row=0,sticky="new")
		sool_frame.grid(row=1,sticky="nsew")
		module_frame.grid(row=2,sticky="new")

		run.grid(row=3,sticky="sew")

		self.rowconfigure(1, weight=1)
		for col_num in range(self.grid_size()[0]):
			self.columnconfigure(col_num, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.master.rowconfigure(0, weight=1)

		self.grid(sticky="nsew")



	def sync_fields(self):
		if self.params.sool_path != "" :
			self.load_manifest(f"{self.params.sool_path}/manifest.xml")

	def browse_CProjectFile(self,thinggy=None):
		filename = filedialog.askopenfilename(filetypes=("CProject file",".cproject"))
		if len(filename) and os.path.exists(filename) :
			self.params.cproject_path = filename

	def browse_sool(self,thinggy=None):
		path = filedialog.askdirectory()
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