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
	`ID`	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	`nome`	TEXT NOT NULL,
	`descrizione`	TEXT,
	`data_creazione`	TEXT,
	`data_modifica`	TEXT,
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
	`ID`	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	`nome`	TEXT NOT NULL,
	`descrizione`	TEXT,
	`data_creazione`	TEXT,
	`data_modifica`	TEXT,
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


def sistemaIndici(c):
    c.execute("SELECT * FROM notes")
    r = c.fetchall()
    for i in range(len(r)):
        if i in r[i]:
            continue
        else:
            c.execute("""UPDATE notes SET ID={} WHERE nome='{}' AND descrizione='{}'
            AND data_creazione='{}' AND data_modifica='{}' AND allegati='{}' AND URIallegato='{}'""".format(i + 1,
                                                                                                            r[i][1],
                                                                                                            r[i][2],
                                                                                                            r[i][3],
                                                                                                            r[i][4],
                                                                                                            r[i][5],
                                                                                                            r[i][6]))


def Salvataggio(mode, titolo, descrizione):
    try:
        conn = sql.connect(os.path.join(path, fn_notes), isolation_level=None)
        c = conn.cursor()
        sistemaIndici(c)
        if mode == "add":
            if "fs" in globals():
                c.execute("INSERT INTO notes VALUES ('{}','{}','{}','{}', '{}', '{}', '{}');".format(len(list(nt.keys())
                                                                                                         ) + 1,
                                                                                                     titolo.get(),
                                                                                                     descrizione.get(
                                                                                                         1.0, END),
                                                                                                     time.strftime(
                                                                                                         "%d/%m/%Y"),
                                                                                                     time.strftime(
                                                                                                         "%d/%m/%Y"),
                                                                                                     fs[len(fs) - 1],
                                                                                                     sf))
            else:
                c.execute("INSERT INTO notes VALUES ('{}','{}','{}','{}', '{}', '{}', '{}');".format(len(list(nt.keys())
                                                                                                         ) + 1,
                                                                                                     titolo.get(),
                                                                                                     descrizione.get(
                                                                                                         1.0, END),
                                                                                                     time.strftime(
                                                                                                         "%d/%m/%Y"),
                                                                                                     time.strftime(
                                                                                                         "%d/%m/%Y"),
                                                                                                     "", ""))
            wa.destroy()
        elif mode == "edit":
            if "fs" in globals() and "lfe" in globals():
                c.execute("""UPDATE notes SET nome='{}', descrizione='{}', data_modifica='{}', allegati='{}',
    URIallegato='{}' WHERE ID={};""".format(titolo.get(), descrizione.get(1.0, END), time.strftime(
                    "%d/%m/%Y"), fs[len(fs) - 1], sf, selItem["text"]))
            else:
                c.execute("""UPDATE notes SET nome='{}', descrizione='{}', data_modifica='{}' WHERE ID={};""".format(
                    titolo.get(), descrizione.get(1.0, END), time.strftime("%d/%m/%Y"), selItem["text"]))
            we.destroy()
        elif mode == "del":
            c.execute("DELETE FROM notes WHERE ID={}".format(selItem["text"]))
        sistemaIndici(c)
        c.close()
        conn.close()
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wn.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore.\n" + str(ex)))


def delete():
    global selItem
    selItem = t.item(t.focus())
    if selItem == "":
        tkmb.showwarning(title=_("Nessuna annotazione selezionata"),
                         messaggio=_("Non è stata selezionata nessuna annotazione. "
                                     "Si prega di selezionarne una per apportarne le modifiche."))
        return ""
    scelta = tkmb.askyesno(title=_("Conferma eliminazione"),
                           message=_("Si è sicuri di voler eliminare la annotazione con titolo {}?").format(
                               selItem["values"][0]))
    if scelta == True:
        Salvataggio("del", "", "")
    else:
        return ""


def file(lf):
    global sf
    sf = filedialog.askopenfilename()
    global fs
    fs = sf.split("/")
    if fs[len(fs) - 1] != "":
        lf["text"] = fs[len(fs) - 1]


def edit():
    global selItem
    selItem = t.item(t.focus())
    if selItem["text"] == "":
        tkmb.showwarning(title=_("Nessuna annotazione selezionata"),
                         message=_("Non è stata selezionata nessuna annotazione. "
                                   "Si prega di selezionarne una per apportarne le modifiche."))
        return ""
    global we
    we = Toplevel()
    we.title(_("Modifica annotazione") + " - School Life Diary")
    we.iconbitmap(r"images/sld_icon_beta.ico")
    we.geometry("750x325+600+200")
    we.configure(bg="white")
    f = LabelFrame(we, text=_("Maschera di modifica"))
    f.pack()
    l = Label(f, text=_("Modificare il titolo dell'annotazione"))
    l.grid(row=0, column=0, padx=10, pady=5)
    vart = StringVar(value=selItem["values"][0])
    et = Entry(f, textvariable=vart)
    et.grid(row=0, column=1, padx=10, pady=2)
    l1 = Label(f, text=_("Modificare il contenuto dell'annotazione"))
    l1.grid(row=1, column=0, padx=10, pady=5)
    varc = StringVar(value="")
    ec = ScrolledText(f, width=50, height=10)
    ec.grid(row=1, column=1, padx=10, pady=2)
    ec.insert(INSERT, selItem["values"][1])
    l2 = Label(f, text=_("Modificare l'allegato (opzionale)"))
    l2.grid(row=2, column=0, padx=10, pady=5)
    fa = Frame(f)
    fa.grid(row=2, column=1)
    global lfe
    lfe = Label(fa, text=_("Nessun file selezionato"))
    if len(selItem["values"]) == 5:
        if selItem["values"][4] != "":
            lfe["text"] = selItem["values"][4]
    pfile = PIL.Image.open(r"icons/pick_file.png")
    ifile = PIL.ImageTk.PhotoImage(pfile)
    btn = Button(fa, text=_("SCEGLI FILE"), image=ifile, compound=LEFT, command=lambda: file(lfe))
    btn.grid(row=0, column=0, padx=10, pady=2)
    lfe.grid(row=0, column=1, padx=10, pady=2)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(we, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: Salvataggio("edit", vart, ec))
    b.pack(padx=10, pady=10)
    we.mainloop()


def add():
    global wa
    wa = Toplevel()
    wa.configure(bg="white")
    wa.title(_("Inserisci annotazione") + " - School Life Diary")
    wa.iconbitmap(r"images/sld_icon_beta.ico")
    wa.geometry("750x325+600+200")
    f = LabelFrame(wa, text=_("Maschera di inserimento"))
    f.pack()
    l = Label(f, text=_("Inserire il titolo della nuova annotazione"))
    l.grid(row=0, column=0, padx=10, pady=5)
    vart = StringVar(value="")
    et = Entry(f, textvariable=vart)
    et.grid(row=0, column=1, padx=10, pady=2)
    l1 = Label(f, text=_("Inserire il contenuto della nuova annotazione"))
    l1.grid(row=1, column=0, padx=10, pady=5)
    varc = StringVar(value="")
    ec = ScrolledText(f, width=50, height=10)
    ec.grid(row=1, column=1, padx=10, pady=2)
    l2 = Label(f, text=_("Inserisci un allegato (opzionale)"))
    l2.grid(row=2, column=0, padx=10, pady=5)
    fa = Frame(f)
    fa.grid(row=2, column=1)
    lf = Label(fa, text=_("Nessun file selezionato"))
    pfile = PIL.Image.open(r"icons/pick_file.png")
    ifile = PIL.ImageTk.PhotoImage(pfile)
    btn = Button(fa, text=_("SCEGLI FILE"), image=ifile, compound=LEFT, command=lambda: file(lf))
    btn.grid(row=0, column=0, padx=10, pady=2)
    lf.grid(row=0, column=1, padx=10, pady=2)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(wa, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: Salvataggio("add", vart, ec))
    b.pack(padx=10, pady=10)
    wa.mainloop()


# INIZIALIZZA DATI
def inizializza():
    global nt
    nt = {}
    conn = sql.connect(os.path.join(path, fn_notes), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    sr = c.fetchall()
    for row in sr:
        nt[row[0]] = {"nome": row[1], "descrizione": row[2], "data_creazione": row[3], "data_modifica": row[4],
                      "allegati": row[5], "URIallegato": row[6]}
    for r in nt:
        for i in nt[r]:
            if nt[r][i] == None:
                nt[r][i] = ""
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
    patt = PIL.Image.open(r"icons/paper-clip.png")
    iatt = PIL.ImageTk.PhotoImage(patt)
    aMenu.delete(4)
    if len(event.widget.item(event.widget.focus())["values"]) == 5:
        if event.widget.item(event.widget.focus())["values"][4] != "":
            aMenu.add_command(label=_("Apri Allegato"), image=iatt, compound="left",
                              command=lambda: on_double_click(event))
    else:
        aMenu.add_separator()
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
    wn.iconbitmap(r"images/sld_icon_beta.ico")
    wn.configure(bg="white")
    wn.geometry("850x350+600+200")
    iAdd = PhotoImage(file=r"icons/add.png")
    iEdit = PhotoImage(file=r"icons/edit.png")
    iDel = PhotoImage(file=r"icons/delete.png")
    patt = PIL.Image.open(r"icons/paper-clip.png")
    iatt = PIL.ImageTk.PhotoImage(patt)
    global aMenu
    aMenu = Menu(wn, tearoff=0)
    aMenu.add_command(label=_('Aggiungi'), image=iAdd, compound="left",
                      command=add)
    aMenu.add_command(label=_('Modifica'), image=iEdit, compound="left",
                      command=edit)
    aMenu.add_command(label=_('Elimina'), image=iDel, compound="left", command=delete)
    aMenu.add_separator()
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
    t.bind("<Double-Button-1>", on_double_click)
    t.bind("<Button-3>", popup)
    for x in list(nt.keys()):
        if ("allegati" in list(nt[x].keys())) and (nt[x]["allegati"] != ""):
            t.insert("", x, text=x, values=[nt[x]["nome"],
                                            nt[x]["descrizione"],
                                            nt[x]["data_creazione"],
                                            nt[x]["data_modifica"],
                                            nt[x]["allegati"]], image=iatt)
        else:
            ia = None
            t.insert("", x, text=x, values=[nt[x]["nome"],
                                            nt[x]["descrizione"],
                                            nt[x]["data_creazione"],
                                            nt[x]["data_modifica"]])
    li = Label(wn, text=_("Per aggiungere una annotazione, usa il tasto destro del mouse su uno spazio "
                          "vuoto della finestra.\nPer aprire l'allegato di una annotazione, fai doppio "
                          "click sulla riga corrispondente.\nPer modificare o eliminare una annotazione, "
                          "selezionare una riga e poi premere il tasto destro del mouse"))
    li.pack()
    wn.bind("<Button-3>", popup2)
    wn.mainloop()
