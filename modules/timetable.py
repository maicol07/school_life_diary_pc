import os.path
import sqlite3 as sql

import PIL.Image
import PIL.ImageTk

from common import variables, init

global path
path = variables.path
module_name = __name__.replace("_", "")
if "." in module_name:
    module_name = module_name[module_name.find(".") + 1:]

conn, c = init.connect_database()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timetable';")
ris = c.fetchall()
if not (len(ris) == 1):
    if not (os.path.exists(os.path.join(path, "data.db"))):
        fm = open(os.path.join(path, "data.db"), "w")
        fm.close()
    c.execute(
        """CREATE TABLE "timetable" ( `ID` INTEGER UNIQUE, `Lun` TEXT, `Mar` TEXT, `Mer` TEXT, `Gio` TEXT, 
        `Ven` TEXT, `Sab` TEXT, PRIMARY KEY(`ID`) );""")
init.close_database(conn, c)

from tkinter import *
from tkinter.ttk import *
from tkinter import Toplevel
import tkinter.messagebox as tkmb


def Salvataggio(matl, matm, matmm, matg, matv, mats):
    """
        Salva l'orario nel database, modificando una sola riga (ora).

        Parametri
        ----------
        :param matl : (string)
            Materia del Lunedì.
        :param matm : (string)
            Materia del Martedì.
        :param matmm : (string)
            Materia del Mercoledì.
        :param matg : (string)
            Materia del Giovedì.
        :param matv : (string)
            Materia del Venerdì.
        :param mats : (string)
            Materia del Sabato.

        Ritorna
        -------
        Niente
            """
    try:
        connection, cur = conn, c
        gg = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab"]
        mat = [matl, matm, matmm, matg, matv, mats]
        for i in range(len(mat)):
            cur.execute("""UPDATE timetable SET {} = '{}' WHERE ID={}; """.format(gg[i], mat[i], sel["text"][0]))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wtc.destroy()
        wt.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore.\n"
                                 "Errore: {}").format(ex))


def updtcblist(e, m):
    """
        Inserisce dentro il menu a tendina le materie.

        Parametri
        ----------
        :param e : (Combobox)
            Menu a tendina, inizialmente vuoto, riempito con questa funzione
        :param m : (list)
            Lista materie.

        Ritorna
        -------
        Niente
            """
    l = []
    for i in m:
        l.append(i[1])
    l.sort()
    e["values"] = l


def cambia_orario():
    """
        Cambia una riga dell'orario

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
    """
    global sel
    sel = tt.item(tt.focus())
    if sel["text"] == "":
        tkmb.showwarning(title=_("Nessuna riga selezionata!"),
                         message=_("Non è stata selezionata nessuna riga. Si prega di selezionarne una per apportare "
                                   "modifiche."))
        return
    global wtc, matconn, matc
    wtc = Toplevel()
    variables.change_window_bg(wtc)
    wtc.title(_("Modifica Orario - Orario scolastico") + " - School Life Diary")
    wtc.iconbitmap(r"images/school_life_diary.ico")
    wtc.geometry("700x200+600+250")
    l = Label(wtc, text=_("Inserire le materie da visualizzare."))
    l.pack(padx=10, pady=10)
    try:
        matconn, matc = conn, c
        matc.execute("SELECT * FROM subjects")
        mat = matc.fetchall()
    except Exception as ex:
        tkmb.showerror(title=_("Nessuna materia inserita!"),
                       message=_(
                           "Errore! Nessuna materia inserita. Inserire delle materie dalla sezione materie!\nErrore "
                           "specifico: {}").format(
                           str(ex)))
    dg = {1: _("Lunedì"), 2: _("Martedì"), 3: _("Mercoledì"), 4: _("Giovedì"), 5: _("Venerdì"), 6: _("Sabato")}
    f = LabelFrame(wtc, text=_("Maschera di modifica"))
    f.pack()
    for i in dg:
        etichetta_giorno = Label(f, text=dg[i])
        etichetta_giorno.grid(row=0, column=i)
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
    b = Button(f, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio(el.get(), em.get(), emm.get(), eg.get(), ev.get(), es.get()))
    b.grid(row=0, column=0, padx=10, pady=10)
    wtc.mainloop()


def inizializza():
    """
        Inizializzazione modulo orario:
            • Crea dizionario con tutte l'orario, recuperate dal database.
            • Crea dizionario con tutte le impostazioni

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    ## INSTALLAZIONE LINGUA ##
    init.Language(module_name)
    global ds
    global dt
    ds = {}
    c.execute("SELECT * FROM settings")
    sr = c.fetchall()
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
            cursor.execute("""INSERT INTO timetable (Lun, Mar, Mer, Gio, Ven, Sab)
            VALUES ("", "", "", "", "", ""); """)
            for a in range(9):
                l = []
                for x in range(6):
                    l.append("")
                dt[i] = l
    return dt


# MENU TASTO DESTRO
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
    if event.widget != tt:
        return
    # display the popup menu
    try:
        aMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        aMenu.grab_release()


def creaFinestra():
    """
        Crea la finestra dell'orario.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    global conn, c
    conn, c = init.connect_database()
    global dt
    dt = inizializza()
    global wt
    wt = Toplevel()
    variables.change_window_bg(wt)
    wt.title(_("Orario scolastico") + " - School Life Diary")
    wt.iconbitmap(r"images/school_life_diary.ico")
    wt.geometry("700x300+600+250")
    ft = Frame(wt)
    ft.pack()
    try:
        mat_conn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
        mat_cur = mat_conn.cursor()
        mat_cur.execute("SELECT * FROM subjects")
        mat = mat_cur.fetchall()
        listmat = []
        for i in mat:
            listmat.append(i[1])
        listmat.sort()
    except Exception as ex:
        tkmb.showerror(title=_("Nessuna materia inserita!"),
                       message=_(
                           "Errore! Nessuna materia inserita. Inserire delle materie dalla sezione materie!\nErrore "
                           "specifico: {}").format(
                           str(ex)))
        wt.destroy()
        return
    x = ds["ORE_MAX_GIORNATA"][0]

    # Creazione dei floating menu

    i_edit = PhotoImage(file=r"icons/edit.png")
    global aMenu
    aMenu = Menu(wt, tearoff=0)
    aMenu.add_command(label=_('Modifica riga'), image=i_edit, compound="left",
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
    tt.heading("ven", text=_("Venerdì"))
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
        "Per modificare l'orario, fai doppio click o usa il tasto destro del mouse su una riga e inserisci le materie "
        "dell'ora corrispondente."))
    li.pack()
    wt.focus()
    wt.mainloop()
