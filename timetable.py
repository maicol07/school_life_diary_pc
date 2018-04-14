import sqlite3 as sql

import PIL.Image
import PIL.ImageTk
import ctypes
import gettext
import locale
import os.path

global path
global fn_set
global fn_time
global dt
fn_set = "settings.db"
fn_time = "timetable.db"
path = os.path.expanduser(r'~\Documents\School Life Diary')
if not (os.path.exists(os.path.join(path, fn_time))):
    fm = open(os.path.join(path, fn_time), "w")
    fm.close()
    conn = sql.connect(os.path.join(path, fn_time), isolation_level=None)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE "timetable" ( `ID` INTEGER UNIQUE, `Lun` TEXT, `Mar` TEXT, `Mer` TEXT, `Gio` TEXT, `Ven` TEXT, `Sab` TEXT, PRIMARY KEY(`ID`) );""")
else:
    conn = sql.connect(os.path.join(path, fn_time), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timetable';")
    ris = c.fetchall()
    if not (len(ris) == 1):
        c.execute(
            """CREATE TABLE "timetable" ( `ID` INTEGER UNIQUE, `Lun` TEXT, `Mar` TEXT, `Mer` TEXT, `Gio` TEXT, `Ven` TEXT, `Sab` TEXT, PRIMARY KEY(`ID`) );""")

# Importazione di Tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import Toplevel
import tkinter.messagebox as tkmb

if not (os.path.exists(os.path.join(path, "language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl = ["en", "it"]
    lg = gettext.translation("timetable", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
else:
    fl = open(os.path.join(path, "language.txt"), "r")
    lgcode = fl.readline()
    lg = gettext.translation('timetable', localedir=os.path.join(path, 'locale'), languages=[lgcode])
lg.install()


def Salvataggio(matl, matm, matmm, matg, matv, mats):
    try:
        conn = sql.connect(os.path.join(path, fn_time), isolation_level=None)
        c = conn.cursor()
        gg = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        mat = [matl, matm, matmm, matg, matv, mats]
        for i in range(len(mat)):
            c.execute("""UPDATE timetable SET {} = '{}' WHERE ID={}; """.format(gg[i], mat[i], sel["text"][0]))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wtc.destroy()
        wt.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore.\nErrore: {}").format(ex))


def updtcblist(e, m):
    l = []
    for i in m:
        l.append(i[1])
    l.sort()
    e["values"] = l


def cambia_orario():
    global sel
    sel = tt.item(tt.focus())
    if sel["text"] == "":
        tkmb.showwarning(title=_("Nessuna riga selezionata!"),
                         message=_("Non è stata selezionata nessuna riga. Si prega di selezionarne una per apportare modifiche."))
        return ""
    global wtc, matconn, matc
    wtc = Toplevel()
    wtc.configure(bg="white")
    wtc.title(_("Modifica Orario - Orario scolastico") + " - School Life Diary")
    wtc.iconbitmap(r"images/school_life_diary.ico")
    wtc.geometry("700x200+600+250")
    l = Label(wtc, text=_("Inserire le materie da visualizzare."))
    l.pack(padx=10, pady=10)
    try:
        matconn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
        matc = matconn.cursor()
        matc.execute("SELECT * FROM subjects")
        mat = matc.fetchall()
    except Exception as ex:
        tkmb.showerror(title=_("Nessuna materia inserita!"),
                       message=_(
                           "Errore! Nessuna materia inserita. Inserire delle materie dalla sezione materie!\nErrore specifico: {}").format(
                           str(ex)))
    dg = {1: _("Lunedì"), 2: _("Martedì"), 3: _("Mercoledì"), 4: _("Giovedì"), 5: _("Venerdì"), 6: _("Sabato")}
    f=LabelFrame(wtc, text=_("Maschera di modifica"))
    f.pack()
    for i in dg:
        lg = Label(f, text=dg[i])
        lg.grid(row=0, column=i)
    lo = Label(f, text=sel["text"])
    lo.grid(row=1, column=0)

    # Creazione di varie combobox (una per ogni giorno), 6 in totale

    el = Combobox(f, postcommand=lambda: updtcblist(el, mat), width=10)
    el.set(sel["values"][0])
    el.grid(row=1, column=1, padx=10, pady=10)
    em = Combobox(f, postcommand=lambda: updtcblist(em, mat), width=10)
    em.set(sel["values"][1])
    em.grid(row=1, column=2, padx=10, pady=10)
    emm = Combobox(f, postcommand=lambda: updtcblist(emm, mat), width=10)
    emm.set(sel["values"][2])
    emm.grid(row=1, column=3, padx=10, pady=10)
    eg = Combobox(f, postcommand=lambda: updtcblist(eg, mat), width=10)
    eg.set(sel["values"][3])
    eg.grid(row=1, column=4, padx=10, pady=10)
    ev = Combobox(f, postcommand=lambda: updtcblist(ev, mat), width=10)
    ev.set(sel["values"][4])
    ev.grid(row=1, column=5, padx=10, pady=10)
    es = Combobox(f, postcommand=lambda: updtcblist(es, mat), width=10)
    es.set(sel["values"][5])
    es.grid(row=1, column=6, padx=10, pady=10)
    f = LabelFrame(wtc, text=_("Azioni"))
    f.pack(padx=10, pady=10)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(f, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: Salvataggio(el.get(), em.get(), emm.get(), eg.get(), ev.get(), es.get()))
    b.grid(row=0, column=0, padx=10, pady=10)
    matc.close()
    matconn.close()
    wtc.mainloop()


def inizializza(c):
    global ds
    ds = {}
    sconn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
    sc = sconn.cursor()
    sc.execute("SELECT * FROM settings")
    sr = sc.fetchall()
    for row in sr:
        ds[row[0]] = (row[1], row[2])
    c.execute("SELECT * FROM timetable")
    r = c.fetchall()
    dt = {}
    # Struttura dizionario: {0:[MatLun,MatMar,MatMer,...],1:[...]}
    if not (r == []):
        for i in r:
            l = []
            for k in i:
                if i.index(k) == 0:
                    continue
                else:
                    l.append(k)
            dt[i[0]] = l
    else:
        for i in range(9):
            c.execute("""INSERT INTO timetable (Lun, Mar, Mer, Gio, Ven, Sab)
            VALUES ("", "", "", "", "", ""); """)
            for a in range(9):
                l = []
                for x in range(6):
                    l.append("")
                dt[i] = l
    sc.close()
    sconn.close()
    return dt


# MENU TASTO DESTRO
def popup(event):
    if event.widget != tt:
        return
    # display the popup menu
    try:
        aMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        aMenu.grab_release()


def creaFinestra():
    """Creazione finestra principale"""
    conn = sql.connect(os.path.join(path, fn_time), isolation_level=None)
    cur = conn.cursor()
    global dt
    dt = inizializza(cur)
    global wt
    wt = Toplevel()
    wt.configure(bg="white")
    wt.title(_("Orario scolastico") + " - School Life Diary")
    wt.iconbitmap(r"images/school_life_diary.ico")
    wt.geometry("700x300+600+250")
    ft = Frame(wt)
    ft.pack()
    try:
        matconn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
        matc = matconn.cursor()
        matc.execute("SELECT * FROM subjects")
        mat = matc.fetchall()
        listmat = []
        for i in mat:
            listmat.append(i[1])
        listmat.sort()
    except Exception as ex:
        tkmb.showerror(title=_("Nessuna materia inserita!"),
                       message=_(
                           "Errore! Nessuna materia inserita. Inserire delle materie dalla sezione materie!\nErrore specifico: {}").format(
                           str(ex)))
        wt.destroy()
        return
    x = ds["ORE_MAX_GIORNATA"][0]

    # Creazione dei floating menu

    iEdit = PhotoImage(file=r"icons/edit.png")
    global aMenu
    aMenu = Menu(wt, tearoff=0)
    aMenu.add_command(label=_('Modifica riga'), image=iEdit, compound="left",
                      command=cambia_orario)

    global tt
    tt = Treeview(wt)
    tt.pack(padx=10, pady=10)
    tt["columns"] = ("lun", "mar", "mer", "gio", "ven", "sab")
    tt.column("#0", width=75)
    tt.heading("lun", text=_("Lunedì"))
    tt.column("lun", anchor=CENTER, width=90)
    tt.heading("mar", text=_("Martedì"))
    tt.column("mar", anchor=CENTER, width=90)
    tt.heading("mer", text=_("Mercoledì"))
    tt.column("mer", anchor=CENTER, width=90)
    tt.heading("gio", text=_("Giovedì"))
    tt.column("gio", anchor=CENTER, width=90)
    tt.heading("ven", text=("Venerdì"))
    tt.column("ven", anchor=CENTER, width=90)
    tt.heading("sab", text=_("Sabato"))
    tt.column("sab", anchor=CENTER, width=90)
    tt.pack(padx=10, pady=10)
    tt.bind("<Double-Button-1>", lambda e: cambia_orario())
    tt.bind("<Button-3>", popup)
    for i in range(1, int(x) + 1):
        tt.insert("", i, text=_("{}° ora").format(i), values=[dt[i][0],
                                                           dt[i][1],
                                                           dt[i][2],
                                                           dt[i][3],
                                                           dt[i][4],
                                                           dt[i][5]])
    li = Label(wt, text=_(
        "Per modificare l'orario, fai doppio click o usa il tasto destro del mouse su una riga e inserisci le materie dell'ora corrispondente."))
    li.pack()
    cur.close()
    conn.close()
    wt.focus()
    wt.mainloop()
