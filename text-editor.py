from tkinter import Tk, Label, Button, Text, Entry, Menu, StringVar, W, E, S, N, END, filedialog, messagebox
import json

class Editor:

	def __init__(self, master):
		self.master = master
		master.title("Shade's Text Editor")
		master.geometry("500x500")
		master.protocol("WM_DELETE_WINDOW", self.closing_handler)
		self.file = StringVar()
		self.file.set("Untitled")
		self.file_name = Label(master, textvariable=self.file)
		vcmd = master.register(self.validate)
		self.text_box = Text(master)
		# self.save_button = Button(master, text="Save", command=lambda: self.save())
		# self.open_button = Button(master, text="Open", command=lambda: self.open())

		# BINDINGS

		self.text_box.bind("<Control-s>", self.save)
		self.text_box.bind("<Control-o>", self.open)
		self.text_box.bind("<Control-S>", self.save_as)
		self.text_box.bind("<Control-z>", self.undo)
		self.text_box.bind("<Control-y>", self.redo)
		# MENUS
		self.menubar = Menu(master)

		# FILE MENU
		self.filemenu = Menu(self.menubar)
		self.filemenu.add_command(label="Open", command=self.open)
		self.filemenu.add_command(label="Save", command=self.save)
		self.filemenu.add_command(label="Save As", command=self.save_as)
		self.filemenu.add_command(label="Undo", command=self.undo)
		self.filemenu.add_command(label="Redo", command=self.redo)
		self.menubar.add_cascade(label="File", menu=self.filemenu)

		# SETTINGS MENU
		self.settings = Menu(self.menubar)
		self.settings.add_command(label="Change Theme", command=self.change_theme)
		self.menubar.add_cascade(label="Settings", menu=self.settings)


		# LAYOUT
		self.file_name.pack()
		self.text_box.pack()
		with open("config.json") as f:
			data = json.loads(f.read())
		if "theme" not in data:
			pass
		else:
			if data["theme"] == "#585251":
				font = "#FFFFFF"
			else:
				font = "#585251"
			self.text_box.config(bg=data["theme"], fg=font)
			self.master.config(bg=data["theme"])
			self.file_name.config(bg=data["theme"], fg=font)
		# self.file_name.grid(row=1, column=1)
		# self.save_button.grid(row=3)
		# self.open_button.grid(row=4)
		master.config(menu=self.menubar)

	def validate(self, new_text):
		# if not new_text: # the field is being cleared
	 #        self.test = 0
	 #        return True

	    try:
	        self.test = str(new_text)
	        return True
	    except ValueError:
	        return False

	def save(self, event=None):
		if self.file.get() == "Untitled":
			self.save_as()
		else:
			with open(self.file.get(), "w") as f:
				f.write(self.text_box.get(1.0, END))

	def save_as(self, event=None):
		file = filedialog.asksaveasfilename(initialdir="Desktop",title="Select File to Save",filetypes = (("text files","*.txt"),("all files","*.*")))
		with open(file, "w") as f:
				f.write(self.text_box.get(1.0, END))

	def open(self, event=None):
		file = filedialog.askopenfilename(initialdir="Desktop", title='Select File to Open', filetypes=(("textt files", "*.txt"), ("all files", "*.*")))
		with open(file, "r") as f:
			self.text_box.delete(1.0, END)
			self.text_box.insert(1.0, f.read())
			self.file.set(file)

	def undo(self, event=None):
		self.text_box.edit_undo()

	def redo(self, event=None):
		self.text_box.edit_redo()


	def change_theme(self):
		with open("config.json") as f:
			data = json.loads(f.read())
		if self.text_box["background"] == "SystemWindow" or self.text_box["background"] == "#FFFFFF":
			color = "#585251"
			self.text_box.config(bg="#585251", fg="#FFFFFF")
			self.master.config(bg="#585251")
			self.file_name.config(bg="#585251", fg="#FFFFFF")
		else:
			color = "#FFFFFF"
			self.text_box.config(bg="#FFFFFF", fg="#585251")
			self.master.config(bg="#FFFFFF",)
			self.file_name.config(bg="#FFFFFF", fg="#585251")
		data["theme"] = color
		data = json.dumps(data, indent=4)
		with open('config.json', 'w') as f:
			f.write(data)

	def closing_handler(self):
		if self.text_box.edit_modified(): #modified
			response = messagebox.askyesnocancel("Save?", "This document has been modified. Do you want to save changes?") #yes = True, no = False, cancel = None
			if response: #yes/save
				self.save()
				self.master.destroy()
			elif response == False:
				self.master.destroy()
			elif response == None:
				pass
		else:
			self.master.destroy()

root = Tk()
gui = Editor(root)
root.mainloop()


