from tkinter import *
from tkinter.ttk import *

class LabeledInput(Frame):
	def __init__(self, label : str, textvariable : StringVar, master = None ):
		super().__init__(master)

		self.label = Label(self,text=label)
		self.input = Entry(self,textvariable=textvariable)

		self.label.grid(row=0,column=0,stick="w")
		self.input.grid(row=0, column=1, stick="ew")

		self.columnconfigure(1, weight=1)
		self.columnconfigure(0, minsize=130)

	@property
	def text(self) -> str:
		return self.input.get()