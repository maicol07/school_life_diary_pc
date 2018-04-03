import os, os.path, time
import sqlite3 as sql

global nt

nt = {}
'''
NT è un dizionario con la seguente struttura (rappresenta una tabella):
nt={"1":{"colonna1":"valore1","colonna2":"valore2", ...},"2":{...}, ...}
Ogni nota ha un corrispondente ID numerico (la chiave) e l valore è un altro
dizionario che rappresentano i valori delle colonne.
'''

global fn_notes
global path
fn_notes = "notes.db"

path = os.path.expanduser(r'~\Documents\School Life Diary')
if not (os.path.exists(os.path.join(path, fn_notes))):
    fm = open(os.path.join(path, fn_notes), "w")
    fm.close()
    conn = sql.connect(os.path.join(path, fn_notes), isolation_level=None)
    c = conn.cursor()
    c.execute("""CREATE TABLE `notes` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nome`	TEXT NOT NULL,
	`descrizione`	TEXT,
	`data_creazione`	TEXT,
	`data_modifica`	TEXT,
	`mat-link`	TEXT,
	`allegati`	TEXT,
	`URIallegato`	TEXT
);""")
else:
    conn = sql.connect(os.path.join(path, fn_notes), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes';")
    ris = c.fetchall()
    if not (len(ris) == 1):
        c.execute("""CREATE TABLE `notes` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nome`	TEXT NOT NULL,
	`descrizione`	TEXT,
	`data_creazione`	TEXT,
	`data_modifica`	TEXT,
	`mat-link`	TEXT,
	`allegati`	TEXT,
	`URIallegato`	TEXT
);""")

import gettext
import ctypes
import locale

if not (os.path.exists(os.path.join(path, "language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl = ["en", "it"]
    lg = gettext.translation("note", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
else:
    fl = open(os.path.join(path, "language.txt"), "r")
    lgcode = fl.readline()
    lg = gettext.translation('note', localedir=os.path.join(path, 'locale'), languages=[lgcode])
lg.install()
from tkinter import *
from tkinter.scrolledtext import *
from tkinter import filedialog
import tkinter.messagebox as tkmb
from ttkthemes.themed_style import *
from tkinter.ttk import *
from tkinter import Tk, Toplevel
import PIL.Image, PIL.ImageTk


def Salvataggio(mode, titolo, descrizione):
    try:
        if mode == "add":
            ID = len(nt) + 1
            nt[ID] = {}
            nt[ID]["titolo"] = titolo.get()
            nt[ID]["descrizione"] = descrizione.get(1.0, END)
            nt[ID]["data_creazione"] = time.strftime("%d/%m/%Y")
            nt[ID]["data_modifica"] = time.strftime("%d/%m/%Y")
            if "fs" in globals():
                nt[ID]["allegati"] = fs[len(fs) - 1]
                nt[ID]["URIallegato"] = sf
            wa.destroy()
        elif mode == "edit":
            ID = selItem["text"]
            nt[ID]["titolo"] = titolo.get()
            nt[ID]["descrizione"] = descrizione.get(1.0, END)
            nt[ID]["data_modifica"] = time.strftime("%d/%m/%Y")
            if "fs" in globals() and "lfe" in globals():
                nt[ID]["allegati"] = fs[len(fs) - 1]
                nt[ID]["URIallegato"] = sf
            we.destroy()
        elif mode == "del":
            ID = selItem["text"]
            del nt[ID]
        np.save(os.path.join(path, fn_notes), nt)
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wn.destroy()
        creaFinestra()
    except:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore"))


def delete():
    global selItem
    selItem = t.item(t.focus())
    if selItem == "":
        tkmb.showwarning(title=_("Nessuna annotazione selezionata"),
                         messaggio=_(
                             "Non è stata selezionata nessuna annotazione. Si prega di selezionarne una per apportarne le modifiche."))
        return ""
    scelta = tkmb.askyesno(title=_("Conferma eliminazione"),
                           message=_("Si è sicuri di voler eliminare la annotazione con titolo") + " " +
                                   selItem["values"][0] + "?")
    if scelta == True:
        Salvataggio("del", "", "")
    else:
        return ""


def file(lf):
    global sf
    sf = filedialog.askopenfilename()
    global fs
    fs = sf.split("/")
    lf["text"] = fs[len(fs) - 1]


def edit():
    global selItem
    selItem = t.item(t.focus())
    if selItem["text"] == "":
        tkmb.showwarning(title=_("Nessuna annotazione selezionata"),
                         message=_(
                             "Non è stata selezionata nessuna annotazione. Si prega di selezionarne una per apportarne le modifiche."))
        return ""
    global we
    we = Toplevel()
    we.title(_("Modifica annotazione") + " - School Life Diary")
    we.iconbitmap(r"icons/sld_icon_beta.ico")
    we.geometry("%dx%d+%d+%d" % (450, 200, 600, 200))
    l = Label(we, text=_("Modificare il titolo dell\'annotazione"))
    l.pack(padx=10, pady=5)
    vart = StringVar(value=selItem["values"][0])
    et = Entry(we, textvariable=vart)
    et.pack(padx=10, pady=2)
    l1 = Label(we, text=_("Modificare il contenuto dell'annotazione"))
    l1.pack(padx=10, pady=5)
    varc = StringVar(value="")
    ec = ScrolledText(we, width=50, height=10)
    ec.pack(padx=10, pady=2)
    ec.insert(INSERT, selItem["values"][1])
    l2 = Label(we, text=_("Modificare l'allegato (opzionale)"))
    l2.pack(padx=10, pady=5)
    fa = Frame(we)
    fa.pack()
    global lfe
    lfe = Label(fa, text=_("Nessun file selezionato"))
    if selItem["values"][4] != "":
        lfe["text"] = selItem["values"][4]
    btn = Button(fa, text=_("SCEGLI FILE"), command=lambda: file(lfe))
    btn.grid(row=0, column=0, padx=10, pady=2)
    lfe.grid(row=0, column=1, padx=10, pady=2)
    b = Button(wa, text=_("SALVA"), command=lambda: Salvataggio("edit", vart, ec))
    b.pack(padx=10, pady=10)
    we.mainloop()


def add():
    global wa
    wa = Toplevel()
    wa.title(_("Inserisci annotazione") + " - School Life Diary")
    wa.iconbitmap(r"icons/sld_icon_beta.ico")
    wa.geometry("510x360+600+200")
    l = Label(wa, text=_("Inserire il titolo della nuova annotazione"))
    l.pack(padx=10, pady=5)
    vart = StringVar(value="")
    et = Entry(wa, textvariable=vart)
    et.pack(padx=10, pady=2)
    l1 = Label(wa, text=_("Inserire il contenuto della nuova annotazione"))
    l1.pack(padx=10, pady=5)
    varc = StringVar(value="")
    ec = ScrolledText(wa, width=50, height=10)
    ec.pack(padx=10, pady=2)
    l2 = Label(wa, text=_("Inserisci un allegato (opzionale)"))
    l2.pack(padx=10, pady=5)
    fa = Frame(wa)
    fa.pack()
    lf = Label(fa, text=_("Nessun file selezionato"))
    btn = Button(fa, text=_("SCEGLI FILE"), command=lambda: file(lf))
    btn.grid(row=0, column=0, padx=10, pady=2)
    lf.grid(row=0, column=1, padx=10, pady=2)
    b = Button(wa, text=_("SALVA"), command=lambda: Salvataggio("add", vart, ec))
    b.pack(padx=10, pady=10)
    wa.mainloop()


# INIZIALIZZA DATI
def inizializza():
    global prof
    prof = {}
    conn = sql.connect(os.path.join(path, fn_notes), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    sr = c.fetchall()
    for row in sr:
        prof[row[0]] = {"nome": row[1], "descrizione": row[2], "data_creazione": row[3], "data_modifica": row[4],
                        "mat-link": row[5], "allegati":row[6], "URIAllegato":row[7]}
    for r in prof:
        for i in prof[r]:
            if prof[r][i] == None:
                prof[r][i] = ""
    c.close()



def on_double_click(event):
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    idn = item['text']
    url = nt[idn]["URIallegato"]
    os.startfile(url)


# MENU TASTO DESTRO
def popup(event):
    if event.widget != t:
        return
    # display the popup menu
    try:
        aMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        aMenu.grab_release()


def popup2(event):
    if event.widget != wn:
        return
    # display the popup menu
    try:
        bMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        bMenu.grab_release()


def creaFinestra():
    global wn
    wn = Toplevel()
    inizializza()
    wn.title(_("Annotazioni") + " - School Life Diary")
    wn.iconbitmap(r"icons/sld_icon_beta.ico")
    wn.geometry("850x350+600+200")
    iAdd = PhotoImage(file=r"icons/add.png")
    iEdit = PhotoImage(file=r"icons/edit.png")
    iDel = PhotoImage(file=r"icons/delete.png")
    global aMenu
    aMenu = Menu(wn, tearoff=0)
    aMenu.add_command(label=_('Aggiungi'), image=iAdd, compound="left",
                      command=add)
    aMenu.add_command(label=_('Modifica'), image=iEdit, compound="left",
                      command=edit)
    aMenu.add_command(label=_('Elimina'), image=iDel, compound="left",
                      command=delete)
    global bMenu
    bMenu = Menu(wn, tearoff=0)
    bMenu.add_command(label=_('Aggiungi'), image=iAdd, compound="left",
                      command=add)
    f = Frame(wn)
    f.pack()
    global t
    t = Treeview(f)
    t["columns"] = ("titolo", "descrizione", "data1", "data2", "allegati")
    t.heading("#0", text=_("ID"))
    t.column("#0", width=50)
    t.heading("titolo", text=_("Titolo"))
    t.heading("descrizione", text=_("Descrizione"))
    t.heading("data1", text=_("Data Creazione"))
    t.column("data1", width=100)
    t.heading("data2", text=_("Data Ultima Modifica"))
    t.column("data2", width=150)
    t.heading("allegati", text=_("Allegati"))
    t.column("allegati", width=125)
    t.pack(padx=10, pady=10)
    patt = PIL.Image.open(r"icons/paper-clip.png")
    iatt = PIL.ImageTk.PhotoImage(patt)
    t.bind("<Double-Button-1>", on_double_click)
    t.bind("<Button-3>", popup)
    for x in list(nt.keys()):
        if ("allegati" in list(nt[x].keys())) and (nt[x]["allegati"] != ""):
            t.insert("", x, text=x, values=[nt[x]["titolo"],
                                            nt[x]["descrizione"],
                                            nt[x]["data_creazione"],
                                            nt[x]["data_modifica"],
                                            nt[x]["allegati"]], image=iatt)
        else:
            ia = None
            t.insert("", x, text=x, values=[nt[x]["titolo"],
                                            nt[x]["descrizione"],
                                            nt[x]["data_creazione"],
                                            nt[x]["data_modifica"]])
    li = Label(wn, text=_(
        "Per aggiungere una annotazione, usa il tasto destro del mouse su uno spazio vuoto della finestra.\nPer aprire l'allegato di una annotazione, fai doppio click sulla riga corrispondente.\nPer modificare o eliminare una annotazione, selezionare una riga e poi premere il tasto destro del mouse"))
    li.pack()
    wn.bind("<Button-3>", popup2)
    wn.mainloop()
