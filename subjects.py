# IMPORTAZIONE MODULI E LIBRERIE
import os.path, gettext, ctypes, locale
import sqlite3 as sql
from tkinter.colorchooser import askcolor
global fn_sub
global path

fn_sub = "subjects.db"

path = os.path.expanduser(r'~\Documents\School Life Diary')
if not(os.path.exists(os.path.join(path,fn_sub))):
    fm=open(os.path.join(path, fn_sub), "w")
    fm.close()
    conn=sql.connect(os.path.join(path, fn_sub),isolation_level=None)
    c=conn.cursor()
    c.execute("""CREATE TABLE "subjects" ( `ID` INTEGER, `name` TEXT, `colour` TEXT, `prof` TEXT , `iprof` TEXT);""")

    
# INSTALLAZIONE LINGUA
if not(os.path.exists(os.path.join(path,"language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode=locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl=["en","it"]
    lg = gettext.translation("subjects", localedir=os.path.join(path,'locale'), languages=[lgcode[0:2]])
else:
    fl=open(os.path.join(path,"language.txt"),"r")
    lgcode=fl.readline()
    lg = gettext.translation('subjects', localedir=os.path.join(path,'locale'), languages=[lgcode])
lg.install()

# IMPORTAZIONE LIBRERIE PER LA GRAFICA
from tkinter import *
import tkinter.messagebox as tkmb
from tkinter.ttk import *
from tkinter import Tk, Toplevel


# INIZIALIZZA DATI
def inizializza():
    global m
    m={}
    conn=sql.connect(os.path.join(path, fn_sub),isolation_level=None)
    c=conn.cursor()
    c.execute("SELECT * FROM subjects")
    sr=c.fetchall()
    for row in sr:
        m[row[0]]={"nome":row[1],"colore":row[2],"prof":row[3],"iprof":row[4]}
    for r in m:
        for i in m[r]:
            if m[r][i]==None:
                m[r][i]=""

def Salvataggio(mode,var):
    try:
        if mode=="add":
            m[var.get()]=[var.get()]
            wa.destroy()
        elif mode=="edit":
            m[old_mat][0]=var.get()
            we.destroy()
        elif mode=="del":
            del m[old_mat]
        np.save(os.path.join(path, fn_sub), m)
        tkmb.showinfo(title=_("Successo!"),
                                    message=_("Salvataggio effettuato con successo!"))
        wim.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                                     message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore")+"\n"+str(ex))

def delete():
    if lb.get(lb.curselection())=="":
        tkmb.showerror(title=_("Nessuna materia selezionata"),
                                     message=_("ERRORE! Nessuna materia selezionata!"))
        return ""
    global old_mat
    old_mat=lb.get(lb.curselection())
    try:
        scelta=tkmb.askyesno(title=_("Conferma eliminazione"),
                                message=_("Si è sicuri di voler eliminare la materia")+" "+old_mat+"?")
    except TypeError:
        scelta=tkmb.askyesno(title=_("Conferma eliminazione"),
                                message=_("Si è sicuri di voler eliminare la materia")+" "+old_mat[0]+"?")
    if scelta==True:
        Salvataggio("del","")
    else:
        return ""

def scegliColore(cc):
    color=askcolor()
    print(color)
    cc["background"]=color[1]
    
def add():
    global wa
    wa=Toplevel()
    wa.configure(background="white")
    wa.title(_("Inserisci materia")+" - School Life Diary")
    wa.iconbitmap("sld_icon_beta.ico")
    wa.geometry("350x300+600+200")
    fam=Labelframe(wa,text=_("Maschera di inserimento"))
    fam.pack(padx=10,pady=10)
    l=Label(fam, text=_("Materia:"))
    l.grid(row=0,column=0,padx=10,pady=10)
    var=StringVar(value="")
    e=Entry(fam, textvariable=var)
    e.grid(row=0,column=1,padx=10,pady=10)
    lc=Label(fam,text=_("Colore"))
    cc=Canvas(fam, bg="light blue", width=50, height=20)
    cc.bind("<Button-1>", lambda e: scegliColore(cc))
    bc.grid(row=2,column=0,padx=1,pady=5)
    cc.grid(row=2,column=1,padx=1,pady=5)
    lp=Label(wa,text=_("Scegli professore"))
    lp.pack(padx=10,pady=10)
    ep=Combobox(wa)
    b=Button(wa, text=_("SALVA"), command=lambda: Salvataggio("add",var))
    b.pack(padx=10,pady=10)
    wa.mainloop()

def edit():
    global old_mat
    old_mat=lb.get(lb.curselection())
    global we
    we=Toplevel()
    we.title(_("Modifica materia")+" - School Life Diary")
    we.iconbitmap("sld_icon_beta.ico")
    we.geometry("%dx%d+%d+%d" % (450, 200, 600, 200))
    l=Label(we, text=_("Inserire la materia da modificare (Vecchia materia:")+" "+old_mat+")")
    l.pack(padx=10,pady=10)
    var=StringVar(value=old_mat)
    e=Entry(we, textvariable=var)
    e.pack(padx=10,pady=10)
    b=Button(we, text=_("SALVA"), command=lambda: Salvataggio("edit",var))
    b.pack(padx=10,pady=10)
    we.mainloop()

# CREA FINESTRA
def creaFinestra():
    global wim
    wim=Toplevel()
    wim.configure(background="white")
    inizializza()
    wim.title(_("Materie")+" - School Life Diary")
    wim.iconbitmap("sld_icon_beta.ico")
    wim.geometry("750x375+600+200")
    s=Style()
    sconn=sql.connect(os.path.join(path, "settings.db"),isolation_level=None)
    sc=sconn.cursor()
    s.theme_use(sc.execute("SELECT value FROM settings WHERE setting='PC_THEME'").fetchone())
    sc.close()
    s.configure("TFrame",background="white")
    s.configure("TLabelframe",background="white")
    s.configure("TLabelframe.Label",background="white")
    s.configure("TLabel",background="white")
    global tm
    tm=Treeview(wim)
    tm.pack(padx=10,pady=10)
    tm["columns"]=("nome","colore","prof")
    tm.heading("#0",text=_("ID"))
    tm.column("#0",width=50)
    tm.heading("nome",text=_("Nome Materia"))
    tm.column("nome",anchor=CENTER)
    tm.heading("colore",text=_("Colore Materia"))
    tm.column("colore",anchor=CENTER)
    tm.heading("prof",text=_("Professore"))
    tm.column("prof",anchor=CENTER)
    tm.pack(padx=10,pady=10)
    tm.bind("<Double-Button-1>", edit)
    for x in list(m.keys()):
        tm.insert("",x,text=x,values=[m[x]["nome"],
                                         m[x]["colore"],
                                         m[x]["prof"]])
    li=Label(wim,text=_("Per modificare una materia, fai doppio click sulla riga corrispondente."))
    li.pack()
    fim2=Labelframe(wim,text=_("Azioni"))
    fim2.pack()
    imageAdd=PhotoImage(file=r"images/add_FAB.png")
    imageDel=PhotoImage(file=r"images/trash_FAB.png")
    bAdd=Button(fim2,image=imageAdd,command=add)
    bAdd.image=imageAdd
    bDel=Button(fim2,image=imageDel,command=delete)
    bAdd.grid(row=0,column=0,padx=10,pady=10)
    bDel.grid(row=0,column=2,padx=10,pady=10)
    print(m)
    wim.focus()
    wim.mainloop()
