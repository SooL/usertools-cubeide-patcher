if __name__ == "__main__" :
	from app.tkMain import MainUI
	import tkinter as tk
	import argparse
	from gui_cube_patcher import run as run_gui

	from app.backend import Parameters

	module_list = ["os","io"]

	parser = argparse.ArgumentParser(description="Patch your project with SooL")
	parser.add_argument("cproject_path", type=str)
	parser.add_argument("sool_path", type=str)
	parser.add_argument("chip", type=str)
	parser.add_argument("--destination","-d",type=str,default="sool")
	parser.add_argument("--gui",action="store_true")
	parser.add_argument("--modules-path",type=str,default="")
	parser.add_argument("--modules","-m",action="extend",nargs="*",type=str,choices=module_list)
	parser.add_argument("--keep-symbols",action="store_true")
	parser.add_argument("--use-links","-l",action="store_true")

	args = parser.parse_args()

	if args.gui :
		run_gui()
	else :
		params = Parameters()
		params.cleanup_debug_symbols = not args.keep_symbols
		params.use_links = args.use_links
		params.sool_chip = args.chip
		params.cproject_path = args.cproject_path
		params.sool_path = args.sool_path
		params.sool_module_path = args.modules_path
		# root = tk.Tk()
		#
		#
		#
		# root.title("SooL Patcher")
		# app = MainUI(root)
		# app.mainloop()
