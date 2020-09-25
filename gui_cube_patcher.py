
from app.tkMain import MainUI
import tkinter as tk

def run():
	root = tk.Tk()

	root.title("SooL Patcher")
	app = MainUI(root)
	app.mainloop()

if __name__ == "__main__" :
	run()