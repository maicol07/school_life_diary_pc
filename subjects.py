import os.path
import numpy as np
global m
global fn_sub
global path
# filename for the file you want to save
fn_sub = "subjects.npy"

path = os.path.expanduser(r'~\Documents\School Life Diary')
# check the directory does not exist
if not(os.path.exists(os.path.join(path,fn_sub))):
    # write the file in the new directory
    m={}
    np.save(os.path.join(path, fn_sub), m)

from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
#Variabili globali
global old_mat

def inizializza():
    #try:
    m=np.load(os.path.join(path, fn_sub)).item()
    #except ValueError:
    #    m={}
def Salvataggio(mode,var):
    try:
        if mode=="add":
            m[var.get()]=[var.get()]
            wa.destroy()
        elif mode=="edit":
            m[old_mat][0]=[var.get()]
            we.destroy()
        elif mode=="del":
            del m[old_mat]
        np.save(os.path.join(path, fn_sub), m)
        tkinter.messagebox.showinfo(title="Successo!", message="Salvataggio effettuato con successo!")
        wim.destroy()
        creaFinestra()
    except:
        tkinter.messagebox.showerror(title="Errore!", message="Si è verificato un errore, riprovare oppure contattare lo sviluppatore")

def delete():
    if lb.get(lb.curselection())=="":
        tkinter.messagebox.showerror(title="Nessuna materia selezionata",
                                     message="ERRORE! Nessuna materia selezionata!")
        return ""
    global old_mat
    old_mat=lb.get(lb.curselection())
    try:
        scelta=tkinter.messagebox.askyesno(title="Conferma eliminazione",
                                message="Si è sicuri di voler eliminare la materia "+old_mat+"?")
    except TypeError:
        scelta=tkinter.messagebox.askyesno(title="Conferma eliminazione",
                                message="Si è sicuri di voler eliminare la materia "+old_mat[0]+"?")
    if scelta==True:
        Salvataggio("del","")
    else:
        return ""
def add():
    global wa
    wa=Toplevel()
    wa.title("Inserisci materia - School Life Diary")
    wa.iconbitmap("sld_icon_beta.ico")
    wa.geometry("%dx%d+%d+%d" % (200, 200, 600, 200))
    l=Label(wa, text="Inserire la nuova materia")
    l.pack(padx=10,pady=10)
    var=StringVar(value="")
    e=Entry(wa, textvariable=var)
    e.pack(padx=10,pady=10)
    b=Button(wa, text="SALVA", command=lambda: Salvataggio("add",var))
    b.pack(padx=10,pady=10)
    wa.mainloop()

def edit():
    global old_mat
    old_mat=lb.get(lb.curselection())
    global we
    we=Toplevel()
    we.title("Modifica materia - School Life Diary")
    we.iconbitmap("sld_icon_beta.ico")
    we.geometry("%dx%d+%d+%d" % (450, 200, 600, 200))
    l=Label(we, text="Inserire la materia da modificare (Vecchia materia: "+old_mat+")")
    l.pack(padx=10,pady=10)
    var=StringVar(value="")
    e=Entry(we, textvariable=var)
    e.pack(padx=10,pady=10)
    b=Button(we, text="SALVA", command=lambda: Salvataggio("edit",var))
    b.pack(padx=10,pady=10)
    we.mainloop()
def riempiListbox(lb):
    for e in m:
        print(m[e])
        lb.insert(list(m.keys()).index(e),m[e][0])
def creaFinestra():
    m=np.load(os.path.join(path, fn_sub)).item()
    global wim
    wim=Toplevel()
    inizializza()
    print(m)
    wim.title("Materie - School Life Diary")
    wim.iconbitmap("sld_icon_beta.ico")
    wim.geometry("%dx%d+%d+%d" % (325, 325, 600, 200))
    s=Style()
    try:
        s.theme_use("vista")
    except:
        s.theme_use()
    fim=Frame(wim)
    fim.pack()
    global lb
    lb=Listbox(fim,selectmode="SINGLE")
    lb.pack(padx=10,pady=10)
    riempiListbox(lb)
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
