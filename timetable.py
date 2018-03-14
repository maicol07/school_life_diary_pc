import sqlite3 as sql
import os.path, gettext, ctypes, locale, PIL.Image, PIL.ImageTk

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
from tkinter import Tk, Toplevel
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


def Salvataggio(p, mat, mode="save"):
    try:
        conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
        c = sconn.cursor()
        matconn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
        matc = matconn.cursor()
        matc.execute("SELECT * FROM subjects")
        lmat = matc.fetchall()
        '''for i in range(len(lmat)):
            if lmat[i[1]] == mat:
                break
            else:
                continue'''
        gg = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        c.execute("""UPDATE subjects SET {} = "{}"
WHERE ID={}; """.format(gg[p[1]], mat, p[0]))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wtc.destroy()
        wt.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_(
                           "Si è verificato un errore, riprovare oppure contattare lo sviluppatore.\nErrore: {}").format(
                           ex))


def updtcblist(e, m):
    l = []
    for i in m:
        l.append(i[1])
    l.sort()
    e["values"] = l


def CambiaOrario(p):  # p è la posizione in coordinate y e x (tupla) del pulsante cliccato
    global wtc
    wtc = Toplevel()
    wtc.configure(bg="white")
    wtc.title(_("Modifica Orario - Orario scolastico") + " - School Life Diary")
    wtc.iconbitmap(r"images/sld_icon_beta.ico")
    wtc.geometry("450x200+600+250")
    l = Label(wtc,
              text=_("Inserire la materia da visualizzare nell'orario la {}° ora del {}.".format(str(p[1]), dg[p[0]])))
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
    e = Combobox(wtc, set=dt[p[0]][p[1]], postcommand=lambda: updtcblist(e, mat))
    e.pack(padx=10, pady=10)
    f = LabelFrame(wtc, text=_("Azioni"))
    f.pack(padx=10, pady=10)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    pdel = PIL.Image.open(r"icons/delete.png")
    idel = PIL.ImageTk.PhotoImage(pdel)
    b = Button(f, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: Salvataggio(p, e.get()))
    b.grid(row=0, column=0, padx=10, pady=10)
    bd = Button(f, text=_("ELIMINA"), image=idel, compound=LEFT, command=lambda: Salvataggio(p, e, mode="del"))
    bd.grid(row=0, column=1, padx=10, pady=10)
    matc.close()
    matconn.close()
    wtc.mainloop()


def inizializza(conn, c):
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
    '''Struttura dizionario:
    {0:[MatLun,MatMar,MatMer,...],1:[...]}'''
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
        for i in range(int(ds["ORE_MAX_GIORNATA"][0])):
            c.execute("""INSERT INTO timetable (Lun, Mar, Mer, Gio, Ven, Sab)
            VALUES ("", "", "", "", "", ""); """)
            for a in range(int(ds["ORE_MAX_GIORNATA"][0])):
                l = []
                for x in range(6):
                    l.append("")
                dt[i] = l
    sc.close()
    sconn.close()
    return dt


def creaFinestra():
    """Creazione finestra principale"""
    conn = sql.connect(os.path.join(path, fn_time), isolation_level=None)
    cur = conn.cursor()
    global dt
    dt = inizializza(conn, cur)
    global wt
    wt = Toplevel()
    wt.configure(bg="white")
    wt.title(_("Orario scolastico") + " - School Life Diary")
    wt.iconbitmap(r"images/sld_icon_beta.ico")
    wt.geometry("600x300+600+250")
    s = Style()
    s.theme_use(ds["PC_THEME"][0])
    s.configure("TFrame", background="white")
    s.configure("TLabel", background="white")
    s.configure("TPhotoimage", background="white")
    s.configure("TLabelframe", background="white")
    s.configure("TLabelframe.Label", background="white")
    ft = Frame(wt)
    ft.pack()
    global dg
    dg = {1: _("Lunedì"), 2: _("Martedì"), 3: _("Mercoledì"), 4: _("Giovedì"), 5: _("Venerdì"), 6: _("Sabato")}
    for i in range(1, len(dg) + 1):
        l = Label(ft, text=dg[i])
        l.grid(row=0, column=i, pady=10, padx=5)
    i = 1
    x = ds["ORE_MAX_GIORNATA"][0]
    for i in range(1, int(x) + 1):
        h = Label(ft, text=str(i) + _("° ora"))
        h.grid(row=i, column=0, padx=5, pady=5)
        i += 1
    for r in range(1, int(x) + 1):
        for c in range(1, 7):
            bh = Button(ft, text=dt[r - 1][c - 1], width=10, command=lambda c=c, r=r: CambiaOrario((c, r)))
            bh.grid(row=r, column=c)
    cur.close()
    conn.close()
    wt.mainloop()
