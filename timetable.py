import numpy as np
import sqlite3 as sql
import os.path, gettext, ctypes, locale
global path
global fn_set
global fn_time
fn_set = "settings.db"
fn_time = "timetable.db"
path = os.path.expanduser(r'~\Documents\School Life Diary')
if not(os.path.exists(os.path.join(path,fn_time))):
    fm=open(os.path.join(path, fn_time), "w")
    fm.close()
    conn=sql.connect(os.path.join(path, fn_time),isolation_level=None)
    c=conn.cursor()
    c.execute("""CREATE TABLE "timetable" ( `ID` INTEGER UNIQUE, `Lun` TEXT, `Mar` TEXT, `Mer` TEXT, `Gio` TEXT, `Ven` TEXT, `Sab` TEXT, PRIMARY KEY(`ID`) );""")
else:
    conn=sql.connect(os.path.join(path, fn_time),isolation_level=None)
    c=conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timetable';")
    ris=c.fetchall()
    if not(len(ris)==1):
        c.execute("""CREATE TABLE "timetable" ( `ID` INTEGER UNIQUE, `Lun` TEXT, `Mar` TEXT, `Mer` TEXT, `Gio` TEXT, `Ven` TEXT, `Sab` TEXT, PRIMARY KEY(`ID`) );""")


#Importazione di Tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import Tk, Toplevel
import tkinter.messagebox as tkmb


if not(os.path.exists(os.path.join(path,"language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode=locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl=["en","it"]
    lg = gettext.translation("timetable", localedir=os.path.join(path,'locale'), languages=[lgcode[0:2]])
else:
    fl=open(os.path.join(path,"language.txt"),"r")
    lgcode=fl.readline()
    lg = gettext.translation('timetable', localedir=os.path.join(path,'locale'), languages=[lgcode])
lg.install()

def Salvataggio(p,var):
    try:
        dt[p]=var.get()
        np.save(os.path.join(path, fn_time), dt)
        tkmb.showinfo(title=_("Successo!"),
                                    message=_("Salvataggio effettuato con successo!"))
        wtc.destroy()
        wt.destroy()
        creaFinestra()
    except:
        tkmb.showerror(title=_("Errore!"), message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore"))

def updtcblist(e,m):
        e["values"]=list(m.keys())
def CambiaOrario(p): #p è la posizione in coordinate y e x (tupla) del pulsante cliccato 
    global wtc
    wtc=Toplevel()
    wtc.title(_("Modifica Orario - Orario scolastico")+" - School Life Diary")
    wtc.iconbitmap(r"images/sld_icon_beta.ico")
    wtc.geometry("450x200+600+250")
    l=Label(wtc, text=_("Inserire la materia da visualizzare nell'orario la {}° ora del {}.".format(str(p[1]),dg[p[0]])))
    l.pack(padx=10,pady=10)
    try:
        m=np.load(os.path.join(path, "subjects.npy")).item()
    except:
        tkmb.showerror(title=_("Nessuna materia inserita!"),
                                     message=_("Errore! Nessuna materia inserita. Inserire delle materie dalla sezione materie!"))
    e=Combobox(wtc, postcommand = lambda: updtcblist(e,m))
    e.pack(padx=10,pady=10)
    b=Button(wtc, text=_("SALVA"), command=lambda: Salvataggio(p,e))
    b.pack(padx=10,pady=10)
    wtc.mainloop()

def inizializza(conn,c):
    global ds
    ds = {}
    sconn=sql.connect(os.path.join(path,fn_set),isolation_level=None)
    sc=sconn.cursor()
    sc.execute("SELECT * FROM settings")
    sr = sc.fetchall()
    for row in sr:
        ds[row[0]] = (row[1], row[2])
    c.execute("SELECT * FROM timetable")
    r=c.fetchall()
    dt={}
    print(r)
    if not(r==[]):
        for i in r:
            l=[]
            print(i)
            print(l)
            for k in i:
                print(k)
                if i.index(k)==0:
                    continue
                else:
                    l.append(k)
            dt[i[0]]=l
    print(dt)
#Creazione finestra
def creaFinestra():
    conn = sql.connect(os.path.join(path, fn_time), isolation_level=None)
    c = conn.cursor()
    inizializza(conn,c)
    global wt
    wt=Toplevel()
    wt.title(_("Orario scolastico")+" - School Life Diary")
    wt.iconbitmap(r"images/sld_icon_beta.ico")
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
    for i in range(1,len(dg)+1):
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
