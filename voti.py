import ctypes
import gettext
import locale
import os.path
import sqlite3 as sql
from tkinter import *
from tkinter import Toplevel
from tkinter.ttk import *

global fn_voti
global path

fn_voti = "voti.db"

path = os.path.expanduser(r'~\Documents\School Life Diary')
if not (os.path.exists(os.path.join(path, fn_voti))):
    fm = open(os.path.join(path, fn_voti), "w")
    fm.close()
    conn = sql.connect(os.path.join(path, fn_voti), isolation_level=None)
    c = conn.cursor()
    c.execute("""CREATE TABLE `voti` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`voto`	REAL NOT NULL,
	`materia`	TEXT NOT NULL,
	`data`	TEXT,
	`periodo`	INTEGER,
	`tipo`	TEXT,
	`peso`	INTEGER,
	`descrizione`	TEXT
);""")
else:
    conn = sql.connect(os.path.join(path, fn_voti), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voti';")
    ris = c.fetchall()
    if not (len(ris) == 1):
        c.execute("""CREATE TABLE `voti` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`voto`	REAL NOT NULL,
	`materia`	TEXT NOT NULL,
	`data`	TEXT,
	`periodo`	INTEGER,
	`tipo`	TEXT,
	`peso`	INTEGER,
	`descrizione`	TEXT
);""")


def install_language():
    """
    Installa la lingua del modulo voti.

    Parametri
    ----------
    Nessuno

    Ritorna
    -------
    Niente
    """
    if not (os.path.exists(os.path.join(path, "language.txt"))):
        windll = ctypes.windll.kernel32
        lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        lg = gettext.translation("voti", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
    else:
        fl = open(os.path.join(path, "language.txt"), "r")
        lgcode = fl.readline()
        lg = gettext.translation('voti', localedir=os.path.join(path, 'locale'), languages=[lgcode])
    lg.install()


def inizializza():
    """
        Inizializzazione modulo voti:
            • Crea dizionario con tutti i voti, recuperate dal database

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    install_language()
    global m
    m = {}
    connection = sql.connect(os.path.join(path, fn_voti), isolation_level=None)
    cur = connection.cursor()
    cur.execute("SELECT * FROM voti")
    sr = cur.fetchall()
    for row in sr:
        m[row[0]] = {"voto": row[1], "materia": row[2], "data": row[3], "periodo": row[4], "tipo": row[5],
                     "peso": row[6], "descrizione": row[7]}
    for r in m:
        for i in m[r]:
            if m[r][i] is None:
                m[r][i] = ""


def popup(event):
    """
        Mostra un menu di opzioni quando viene cliccata una riga della tabella con il tasto destro.

        Parametri
        ----------
        :param event : (treeview callback)
            Parametro che identifica l'evento del cliccare con il tasto destro una annotazione dalla tabella.

        Ritorna
        -------
        Niente
        """
    if event.widget != tv:
        return
    # display the popup menu
    try:
        aMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        aMenu.grab_release()


def popup2(event):
    """
        Mostra un menu di opzioni (solo aggiunta) quando viene cliccato uno spazio vuoto della finestra con il
        tasto destro.

        Parametri
        ----------
        :param event : (treeview callback)
            Parametro che identifica l'evento del cliccare con il tasto destro uno spazio vuoto della finestra.

        Ritorna
        -------
        Niente
        """
    if event.widget != wv:
        return
    # display the popup menu
    try:
        bMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        bMenu.grab_release()


# CREA FINESTRA
def creaFinestra():
    """
        Crea la finestra dell'agenda.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    global wv
    wv = Toplevel()
    wv.configure(background="white")
    inizializza()
    wv.title(_("Voti") + " - School Life Diary")
    wv.iconbitvap(r"images/school_life_diary.ico")
    wv.geometry("750x375+600+200")
    i_add = PhotoImage(file=r"icons/add.png")
    i_edit = PhotoImage(file=r"icons/edit.png")
    i_del = PhotoImage(file=r"icons/delete.png")
    global aMenu
    aMenu = Menu(wv, tearoff=0)
    aMenu.add_command(label=_('Aggiungi'), image=i_add, compound="left",
                      command=add)
    aMenu.add_command(label=_('Modifica'), image=i_edit, compound="left",
                      command=edit)
    aMenu.add_command(label=_('Elimina'), image=i_del, compound="left",
                      command=delete)
    global bMenu
    bMenu = Menu(wv, tearoff=0)
    bMenu.add_command(label=_('Aggiungi'), image=i_add, compound="left",
                      command=add)
    frame_materie = Labelframe(wv, )
    cbm = Combobox()
    global tv
    tv = Treeview(wv)
    tv.pack(padx=10, pady=10)
    tv["columns"] = ("voto", "materia", "data", "periodo", "tipo", "peso", "descrizione")
    tv.heading("#0", text=_("ID"))
    tv.column("#0", width=50)
    tv.heading("nome", text=_("Nome Materia"))
    tv.column("nome", anchor=CENTER)
    tv.heading("colore", text=_("Colore Materia"))
    tv.column("colore", anchor=CENTER)
    tv.heading("prof", text=_("Professore"))
    tv.column("prof", anchor=CENTER)
    tv.pack(padx=10, pady=10)
    tv.bind("<Double-Button-1>", lambda e: edit())
    tv.bind("<Button-3>", popup)
    for x in list(m.keys()):
        tv.insert("", x, text=x, values=[m[x]["nome"],
                                         m[x]["colore"],
                                         m[x]["prof"]])
    li = Label(wv, text=_(
        "Per aggiungere un voto, usa il tasto destro del mouse su uno spazio vuoto della finestra.\nPer "
        "modificare un voto, fai doppio click sulla riga corrispondente.\nPer modificare o eliminare un voto, "
        "selezionare una riga e poi premere il tasto destro del mouse."))
    li.pack()
    wv.bind("<Button-3>", popup2)
    wv.focus()
    conn.close()
    wv.mainloop()
