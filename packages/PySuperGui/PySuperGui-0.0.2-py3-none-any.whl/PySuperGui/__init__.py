import tkinter
import tkinter.ttk

class InvalidValue(Exception):
    pass

class Start:
    def __init__(self, title="PySuperGui",color="white", width=250, height=200):
        try:
            self.Title = title
            self.gui = tkinter.Tk()
            self.gui.configure(bg=color)
            self.gui.title(title)
            self.gui.geometry(str(width) + "x" + str(height) + "+400+200")
            self.Size = str(width) + "x" + str(height) + "+400+200"
            self.gui.resizable(True, True)
        except tkinter.TclError:
            raise InvalidValue("Invalid Size")
    def _gettkIG(self):
        return {"gui":self.gui,"title":self.Title,"size":self.Size}
    def show(self):
        self.gui.mainloop()
    def size(self, SizeX, SizeY):
        try:
            self.Size = str(SizeX) + "x" + str(SizeY) + "+400+200"
            self.gui.geometry(self.Size)
        except tkinter.TclError:
            raise InvalidValue("Invalid Size")
class Frame:
    def __init__(self, gui, color="grey", posX=0.025, posY=0.05, width=0.2, height=0.2):
        info = gui._gettkIG()
        self.Frame = tkinter.Frame(info["gui"], bg=color)
        self.Frame.place(relx=posX, rely=posY, relwidth=width, relheight=height)
    def _gettkIG(self):
        return {"frame":self.Frame}
class TextButton:
    def __init__(self, frame, text="Text", command="", color="white", posX=0, posY=0, width=0.2, height=0.2):
        info = frame._gettkIG()
        if command == "":
            self.Button = tkinter.Button(info["frame"],bg=color , text=text)
        else:
            self.Button = tkinter.Button(info["frame"],bg=color , text=text, command=command)
        self.Button.place(relx=posX, rely=posY, relwidth=width ,relheight=height)
class TextLabel:
    def __init__(self, frame, text="Text", bkColor="grey", textColor="black", posX=0, posY=0, width=0.2, height=0.2):
        info = frame._gettkIG()
        self.Text = tkinter.Label(info["frame"], text=text, bg=bkColor,fg=textColor)
        self.Text.place(relx=posX, rely=posY, relwidth=width, relheight=height)
class TextBox:
    def __init__(self, frame, text="",bkColor="white", textColor="black", posX=0, posY=0, width=0.2, height=0.15):
        info = frame._gettkIG()
        self.TB = tkinter.Entry(info["frame"], bg=bkColor, fg=textColor)
        self.TB.insert(0,text)
        self.TB.place(relx=posX, rely=posY, relwidth=width, relheight=height)
    def getValue(self):
        return self.TB.get()
class CheckBox:
    def __init__(self, frame, text="",command="" ,bkColor="grey", textColor="black", posX=0, posY=0, width=0.2, height=0.15):
        info = frame._gettkIG()
        self.var1 = tkinter.IntVar()
        if command == "":
            self.CB = tkinter.Checkbutton(info["frame"], text=text, bg=bkColor, fg=textColor,variable=self.var1)
        else:
            self.CB = tkinter.Checkbutton(info["frame"], text=text, command=command, bg=bkColor, fg=textColor,variable=self.var1)
        self.CB.place(relx=posX, rely=posY, relwidth=width, relheight=height)
    def getValue(self):
        if self.var1.get() == 0:
            return False
        elif self.var1.get() == 1:
            return True
class ComboBox:
    def __init__(self, frame, values=[],command="", text="", posX=0, posY=0, width=0.2, height=0.15):
        info = frame._gettkIG()
        if command == "":
            self.ComboBox = tkinter.ttk.Combobox(info["frame"], state="READONLY", values=values)
        else:
            self.ComboBox = tkinter.ttk.Combobox(info["frame"], state="READONLY", postcommand=command, values=values)
        self.ComboBox.set(text)
        self.ComboBox.place(relx=posX, rely=posY, relwidth=width, relheight=height)
    def getValue(self):
        return self.ComboBox.get()
