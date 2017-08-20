import os.path
import numpy as np
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
def delete():
    m=0

def add():
    m=0 #Per non far causare un errore nell'avvio del software, ho creato una variabile con valore 0

def edit():
    m=0

def creaFinestra():
    wim=Toplevel()
    wim.title("Materie - School Life Diary")
    wim.iconbitmap("sld_icon_beta.ico")
    wim.geometry("%dx%d+%d+%d" % (325, 325, 200, 100))
    s=Style()
    try:
        s.theme_use("vista")
    except:
        s.theme_use()
    fim=Frame(wim)
    fim.pack()
    m=[]
    lb=Listbox(fim,selectmode="SINGLE")
    for e in m:
        lb.insert(m[e], e)
    lb.pack(padx=10,pady=10)
    fim2=Frame(wim)
    fim2.pack()
    imageAdd=PhotoImage(r"icons/add_FAB.png")
    imageMod=PhotoImage(r"icons/edit_FAB.png")
    imageDel=PhotoImage(r"icons/trash_FAB.png")
    bAdd=Button(fim2,image=imageAdd,command=add)
    bMod=Button(fim2,image=imageMod,command=edit)
    bDel=Button(fim2,image=imageDel,command=delete)
    bAdd.grid(row=0,column=0,padx=10,pady=10)
    bMod.grid(row=0,column=1,padx=10,pady=10)
    bDel.grid(row=0,column=2,padx=10,pady=10)
    wim.mainloop()
