import ctypes
import gettext
import locale
import os
import os.path
import sqlite3 as sql
from tkinter import *
from tkinter import Toplevel
from tkinter.ttk import *

from tk_tools import *

global ag

ag = {}
'''AG è un dizionario con la seguente struttura (rappresenta una tabella): ag={"anno-mese-giorno":{"idevento":{
"titolo":"valoretitolo","descrizione":"valoredescr", "data":"valoredata", "ora":"valoreora" ...}, ...} Ogni nota ha 
un corrispondente ID numerico (la chiave) e l valore è un altro dizionario che rappresentano i valori delle colonne. '''

global fn_agenda
global path
fn_agenda = "agenda.db"

path = os.path.expanduser(r'~\Documents\School Life Diary')
if not (os.path.exists(os.path.join(path, fn_agenda))):
    fm = open(os.path.join(path, fn_agenda), "w")
    fm.close()
    '''conn = sql.connect(os.path.join(path, fn_agenda), isolation_level=None)
    c = conn.cursor()
        c.execute("""CREATE TABLE `{}_{}` (
        `ID`	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
        `nome`	TEXT NOT NULL,
        `descrizione`	TEXT,
        `data_creazione`	TEXT,
        `data_modifica`	TEXT,
        `allegati`	TEXT,
        `URIallegato`	TEXT
    );""")
else:
    conn = sql.connect(os.path.join(path, fn_agenda), isolation_level=None)
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
);""")'''


def install_language():
    """
    Installa la lingua del modulo agenda.

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
        lg = gettext.translation("agenda", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
    else:
        fl = open(os.path.join(path, "language.txt"), "r")
        lgcode = fl.readline()
        lg = gettext.translation('agenda', localedir=os.path.join(path, 'locale'), languages=[lgcode])
    lg.install()


def selezione():
    print(cal.selection)


def inizializza(c):
    """
        Inizializzazione modulo agenda:
            • Crea dizionario con tutti gli eventi, recuperati dal database

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    install_language()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    r = c.fetchall()
    if r == []:
        return False


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
    conn = sql.connect(os.path.join(path, fn_agenda), isolation_level=None)
    c = conn.cursor()
    es = inizializza(c)
    aw = Toplevel()
    aw.title(_("Agenda - School Life Diary"))
    aw.configure(bg="white")
    aw.iconbitmap(r"images/school_life_diary.ico")
    global cal
    cal = Calendar(aw)
    cal.pack()
    cal.add_callback(selezione)
    if not (es is False):
        b = Button(aw, text=_("Visualizza tutto"), )
        b.pack(pady=2)
        t = Treeview(aw)
        t.pack()
    else:
        l = Label(aw, text=_("Nessun evento è stato pianificato."))
        l.pack(pady=10)
    aw.mainloop()
