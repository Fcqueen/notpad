import os 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notpad:
    __root = Tk()
    __thisWidth = 300 
    __thisHeight = 300 
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None
    def __init__(self, **kwargs):
        try :
            self.__root.wm_iconbitmap("Notpad.ico")
        except:
            pass 

        try: 
            self.__thisWidth = kwargs['width']
        except KeyError:
             pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError: 

            pass 
        self.__root.title("Untitled - Notpad")
        screenWidth = self.__root.winfo_screenwidth()

        screenHeight = self.__root.winfo_screenheight()
        positionTop = int(screenHeight / 2 - self.__thisHeight / 2)
        positionRight = int(screenWidth / 2 - self.__thisWidth / 2)
        self.__root.geometry(f'{self.__thisWidth}x{self.__thisHeight}+{positionRight}+{positionTop}')
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Set up Text Area
        self.__thisTextArea.grid(sticky=N+S+E+W)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

        # Add Menu Bar
        self.__root.config(menu=self.__thisMenuBar)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        # Add File Menu
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_command(label="Save As", command=self.__saveAsFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__exitApp)

        # Add Edit Menu
        self.__thisEditMenu.add_command(label="Undo", command=self.__undo)
        self.__thisEditMenu.add_command(label="Redo", command=self.__redo)
        self.__thisEditMenu.add_separator()
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisEditMenu.add_separator()
        self.__thisEditMenu.add_command(label="Select All", command=self.__selectAll)

        # Add Help Menu
        self.__thisHelpMenu.add_command(label="About", command=self.__about)

    def __newFile(self):
        self.__root.title("Untitled - Notpad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __openFile(self):
        file = askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file != "":
            self.__file = file
            self.__root.title(f"{os.path.basename(file)} - Notpad")
            self.__thisTextArea.delete(1.0, END)
            with open(file, "r") as f:
                self.__thisTextArea.insert(1.0, f.read())

    def __saveFile(self):
        if self.__file is None:
            self.__saveAsFile()
        else:
            with open(self.__file, "w") as f:
                f.write(self.__thisTextArea.get(1.0, END))

    def __saveAsFile(self):
        file = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file != "":
            self.__file = file
            with open(file, "w") as f:
                f.write(self.__thisTextArea.get(1.0, END))
            self.__root.title(f"{os.path.basename(file)} - Notpad")

    def __exitApp(self):
        if askyesno("Quit", "Do you want to save changes?"):
            self.__saveFile()
        self.__root.quit()

    def __undo(self):
        try:
            self.__thisTextArea.edit_undo()
        except:
            pass

    def __redo(self):
        try:
            self.__thisTextArea.edit_redo()
        except:
            pass

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def __selectAll(self):
        self.__thisTextArea.tag_add("sel", 1.0, END)
        self.__thisTextArea.mark_set("insert", "1.0")
        self.__thisTextArea.see("insert")

    def __about(self):
        showinfo("Notpad", "A basic Notepad application using Python Tkinter")

    def run(self):
        self.__root.mainloop()

# Run the application
if __name__ == "__main__":
    Notpad(width=600, height=400).run()






