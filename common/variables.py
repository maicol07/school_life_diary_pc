import os.path
import tkinter.messagebox as tkmb
from tkinter.filedialog import *
from tkinter.ttk import Entry, Frame, Button

from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

version = "1.0.0"


def path_init():
    global path
    if not (os.path.exists("path.txt")):
        w = Tk()
        w.title("Select data path")
        w.iconbitmap(r"images/school_life_diary.ico")
        Label(w, text="Select the path where the data folder will be created. If you would like to use the default one,"
                      "then click OK.").pack()
        f = Frame(w)
        f.pack()
        var = StringVar()
        var.set(os.path.expanduser(r'~\Documents'))
        e = Entry(f, textvariable=var, width=45)
        i_folder = Image.open(r"icons\folder.png")
        f_image = ImageTk.PhotoImage(i_folder)
        b = Button(f, image=f_image, compound="left", command=lambda: var.set(askdirectory()))
        e.grid(row=0, column=0)
        b.grid(row=0, column=1, padx=5)
        b_ok = Button(w, text="OK", command=lambda: w.destroy())
        b_ok.pack()
        w.mainloop()
        path = var.get()
        txt = open("path.txt", "w")
        txt.write(path + "\School Life Diary")
        txt.close()
        txt = open("path.txt", "r")
        path = txt.read()
        txt.close()
    else:
        txt = open("path.txt", "r")
        path = txt.read()
        if not (os.path.exists(path)):
            try:
                os.makedirs(path)
            except FileNotFoundError:
                tkmb.showerror(title="Can't find path",
                               message="We couldn't find the path of the app data files.\nTo fix this please type in "
                                       "the file path.txt (if it doesn't exists create it) inside the installation "
                                       "folder the path to your documents folder. To find it right click on documents "
                                       "folder in explorer and then go to path tab. Copy the path and paste inside it "
                                       "the file.")
        txt.close()


def style_init(c=None, w=None):
    """
        Inizializzazione delle variabili globali
        :return:
        """
    global s
    s = ThemedStyle()
    if c is not None:
        s.configure('.', font=c.execute("SELECT value FROM settings WHERE setting='PC_FONT'").fetchone()[0])
        theme = c.execute("SELECT value FROM settings WHERE setting='PC_THEME'").fetchone()[0]
    update_style(theme)
    if w is not None:
        change_window_bg(w)


def change_window_bg(w):
    w.configure(background=color)


def update_style(newtheme=None):
    global color
    s.set_theme(newtheme)
    color = s.lookup("TButton", "background", default="white")
    if color == "SystemButtonFace":
        color = "white"
    s.configure("TFrame", background=color)
    s.configure("TButton", height=100)
    s.configure("TLabel", background=color)
    s.configure("TPhotoimage", background=color)
    s.configure("TLabelframe", background=color)
    s.configure("TLabelframe.Label", background=color)
    s.configure("TScale", background=color)
    s.configure("TCheckbutton", background=color)
