import numpy as np
import os.path
global path
global fn_set
global fn_time
fn_set = "settings.npy"
fn_time = "timetable.npy"
path = os.path.expanduser(r'~\Documents\School Life Diary')
global ds
global dt
ds=np.load(os.path.join(path, fn_set)).item()
try:
    dt=np.load(os.path.join(path, fn_time)).item()
except:
    dt={"ORE_MAX_GIORNATA":ds["ORE_MAX_GIORNATA"]}
#Importazione di Tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import gettext
import ctypes
import locale
if not(os.path.exists(os.path.join(path,"language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode=locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl=["en","it"]
    lg = gettext.translation("settings", localedir='locale', languages=[lgcode[0:2]])
else:
    fl=open(os.path.join(path,"language.txt"),"r")
    lgcode=fl.readline()
    lg = gettext.translation('settings', localedir='locale', languages=[lgcode])
lg.install()

def Salvataggio(p,var):
    try:
        dt[p]=var.get()
        np.save(os.path.join(path, fn_time), dt)
        tkinter.messagebox.showinfo(title=_("Successo!"),
                                    message=_("Salvataggio effettuato con successo!"))
        wtc.destroy()
        wt.destroy()
        creaFinestra()
    except:
        tkinter.messagebox.showerror(title=_("Errore!"), message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore"))

def updtcblist(e,m):
        e["values"]=list(m.keys())
def CambiaOrario(p): #p è la posizione in coordinate y e x (tupla) del pulsante cliccato 
    global wtc
    wtc=Toplevel()
    wtc.title(_("Modifica Orario - Orario scolastico")+" - School Life Diary")
    wtc.iconbitmap("sld_icon_beta.ico")
    wtc.geometry("450x200+600+250")
    l=Label(wtc, text=_("Inserire la materia da visualizzare nell'orario la")+" "+str(p[1])+_("° ora del")+" "+dg[p[0]]+".")
    l.pack(padx=10,pady=10)
    try:
        m=np.load(os.path.join(path, "subjects.npy")).item()
    except:
        tkinter.messagebox.showerror(title=_("Nessuna materia inserita!"),
                                     message=_("Errore! Nessuna materia inserita. Inserire delle materie dalla sezione materie!"))
    e=Combobox(wtc, postcommand = lambda: updtcblist(e,m))
    e.pack(padx=10,pady=10)
    b=Button(wtc, text=_("SALVA"), command=lambda: Salvataggio(p,e))
    b.pack(padx=10,pady=10)
    wtc.mainloop()

def inizializza(dt):
    try:
        dt=np.load(os.path.join(path, fn_time)).item()
    except:
        dt={"ORE_MAX_GIORNATA":ds["ORE_MAX_GIORNATA"]}
    if not(os.path.exists(os.path.join(path, fn_time))):
        dt={}
        dt["ORE_MAX_GIORNATA"]=ds["ORE_MAX_GIORNATA"]
        for r in range(1,ds["ORE_MAX_GIORNATA"]+1):
            for c in range (1,7):
                dt[(c,r)]=""
        np.save(os.path.join(path, fn_time), dt)
    if dt["ORE_MAX_GIORNATA"]!=ds["ORE_MAX_GIORNATA"]:
        dt["ORE_MAX_GIORNATA"]=ds["ORE_MAX_GIORNATA"]
        for r in range(1,ds["ORE_MAX_GIORNATA"]+1):
            for c in range (1,7):
                dt[(c,r)]=""
        np.save(os.path.join(path, fn_time), dt)
    dt=np.load(os.path.join(path, fn_time)).item()
#Creazione finestra
def creaFinestra():
    inizializza(dt)
    global wt
    wt=Toplevel()
    wt.title(_("Orario scolastico")+" - School Life Diary")
    wt.iconbitmap("sld_icon_beta.ico")
    wt.geometry("600x300+600+250")
    s=Style()
    try:
        s.theme_use("vista")
    except:
        s.theme_use()
    ft=Frame(wt)
    ft.pack()
    global dg
    dg={1:_("Lunedì"),2:_("Martedì"),3:_("Mercoledì"),4:_("Giovedì"),5:_("Venerdì"),6:_("Sabato")}
    for i in len(dg):
        l=Label(ft,text=dg[i])
    l.grid(row=0, column=i, pady=10, padx=5)
    i=1
    x=ds["ORE_MAX_GIORNATA"]
    for i in range(1,x+1):
        h=Label(ft, text=str(i)+_("° ora"))
        h.grid(row=i, column=0, padx=5, pady=5)
        i+=1
    for r in range(1,x+1):
        for c in range(1,7):
            bh=Button(ft, text=dt[(c,r)], width=10, command=lambda c=c,r=r: CambiaOrario((c,r)))
            bh.grid(row=r, column=c)
    wt.mainloop()
