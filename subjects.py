import os.path
import numpy as np
global m
global fn_sub
global path
m=[]
# filename for the file you want to save
fn_sub = "subjects.npy"

path = os.path.expanduser(r'~\Documents\School Life Diary')
# check the directory does not exist
if not(os.path.exists(os.path.join(path,fn_sub))):
    # write the file in the new directory
    np.save(os.path.join(path, fn_sub), m)

from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
#Variabili globali
global old_mat

def inizializza():
    m=np.load(os.path.join(path, fn_sub)).item()

def Salvataggio(mode,var):
    try:
        if mod=="add":
            m.append(var.get())
        elif mod=="edit":
            m[old_mat]=var.get()
        elif mod=="del":
            del m[old_mat]
        np.save(os.path.join(path, fn_sub), m)
        tkinter.messagebox.showinfo(title="Successo!", message="Salvataggio effettuato con successo!")
        wa.destroy()
        wim.destroy()
        creaFinestra()
    except:
        tkinter.messagebox.showerror(title="Errore!", message="Si è verificato un errore, riprovare oppure contattare lo sviluppatore")

def delete():
    old_mat=lb.get(lb.curselection())
    if old_mat=="":
        tkinter.messagebox.showwarning(title="Nessuna materia selezionata",
                                       message="Attenzione! Non hai selezionato nessuna materia!")
    scelta=tkinter.messagebox.askyesno(title="Conferma eliminazione",
                                message="Si è sicuri di voler eliminare la materia"+old_mat+"?")
    if scelta==True:
        Salvataggio("del",var)
    else:
        return ""
        
def add():
    wa=TopLevel()
    wa.title("Inserisci materia - School Life Diary")
    wa.iconbitmap("sld_icon_beta.ico")
    wa.geometry("%dx%d+%d+%d" % (450, 200, 600, 250))
    l=Label(wa, text="Inserire la nuova materia")
    l.pack(padx=10,pady=10)
    var=StringVar(value="")
    e=Entry(wa, textvariable=var)
    e.pack(padx=10,pady=10)
    b=Button(wa, text="SALVA", command=lambda: Salvataggio("add",var))
    b.pack(padx=10,pady=10)
    wa.mainloop()

def edit():
    old_mat=lb.get(lb.curselection())
    we=TopLevel()
    we.title("Modifica materia - School Life Diary")
    we.iconbitmap("sld_icon_beta.ico")
    we.geometry("%dx%d+%d+%d" % (450, 200, 600, 250))
    l=Label(we, text="Inserire la materia da modificare (Vecchia materia: "+old_mat+")")
    l.pack(padx=10,pady=10)
    var=StringVar(value="")
    e=Entry(we, textvariable=var)
    e.pack(padx=10,pady=10)
    b=Button(we, text="SALVA", command=lambda: Salvataggio("mod",var))
    b.pack(padx=10,pady=10)
    we.mainloop()

def creaFinestra():
    wim=Toplevel()
    inizializza()
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
    imageAdd=PhotoImage(file=r"images/add_FAB.png")
    imageMod=PhotoImage(file=r"images/mod_FAB.png")
    imageDel=PhotoImage(file=r"images/trash_FAB.png")
    bAdd=Button(fim2,image=imageAdd,command=add)
    bAdd.image=imageAdd
    bMod=Button(fim2,image=imageMod,command=edit)
    bDel=Button(fim2,image=imageDel,command=delete)
    bAdd.grid(row=0,column=0,padx=10,pady=10)
    bMod.grid(row=0,column=1,padx=10,pady=10)
    bDel.grid(row=0,column=2,padx=10,pady=10)
    wim.mainloop()
