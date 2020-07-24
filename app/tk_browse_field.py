from tkinter import *
from tkinter.ttk import *

class BrowseField(Frame):
	def __init__(self, label : str, textvariable : StringVar, command, master = None, on_edit = None, ):
		super().__init__(master)

		self.label = Label(self, text=label)
		self.entry = Entry(self, textvariable=textvariable)
		self.browse = Button(self, text="...", command=command)

		self.label.grid(column=0,row=0,stick="W")
		self.entry.grid(column=1,row=0, stick="WE")
		self.browse.grid(column=2,row=0,stick = "E",padx=(5,0))

		self.columnconfigure(1, weight=1)
		self.columnconfigure(0, minsize=130)

		if on_edit is not None :
			textvariable.trace("w",lambda name, index, mode, var=textvariable : on_edit(textvariable))


