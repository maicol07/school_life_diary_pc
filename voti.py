import sys

### IMPOSTAZIONE PERCORSO LIBRERIE ESTERNE ###
sys.path.insert(0, 'lib')

import ctypes
import gettext
import locale
import os.path
import sqlite3 as sql
import tkinter.messagebox as tkmb
from tkinter import *
from tkinter import Toplevel
from tkinter.ttk import *

import PIL.Image
import PIL.ImageTk

import datepicker

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
        lg = gettext.translation("voti", localedir=os.path.join(path, 'locale'), languages=[lgcode])
    else:
        fl = open(os.path.join(path, "language.txt"), "r")
        lgcode = fl.readline()
        lg = gettext.translation('voti', localedir=os.path.join(path, 'locale'), languages=[lgcode])
    lg.install()
    locale.setlocale(locale.LC_ALL, lgcode)


def updatecombobox(cb, tt=True):
    """
    Aggiorna le opzioni della combobox con le materie salvate nel database

    Parametri
    ----------
    :param cb: (ttk.combobox)
        Combobox che conterrà tutte le materie. Inizialmente vuota.
    :param tt: (bool)
        Valore booleano che determina se è selezionato Tutte le materie o una materia specifica.

    Ritorna
    --------
    Niente
    """
    matconn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
    matc = matconn.cursor()
    matc.execute("SELECT * FROM subjects")
    r = matc.fetchall()
    if tt is True:
        l = [_("Tutte le materie")]
    else:
        l = []
    if not (r == []):
        for i in r:
            l.append(i[1])
    cb["values"] = l


def sistemaIndici(cursor):
    """
        Corregge possibili errori negli indici dei voti, salvati nel database.

        Parametri
        ----------
        :param cursor : (sqlite3.Cursor)
            Cursore che effettua operazioni sul database.

        Ritorna
        -------
        Niente
            """
    cursor.execute("SELECT * FROM voti")
    r = cursor.fetchall()
    for i in range(len(r)):
        if i in r[i]:
            continue
        else:
            cursor.execute("""UPDATE voti SET ID={} WHERE voto='{}' AND materia='{}'
            AND data='{}' AND tipo='{}' AND peso='{}' AND descrizione='{}'""".format(i + 1, r[i][1], r[i][2], r[i][3],
                                                                                     r[i][5], r[i][6], r[i][7]))


def Salvataggio(mode, voto, materia, data, periodo, tipo, descrizione, peso="100", idx=0):
    """
        Salva il voto nel database, in base all'azione scelta (aggiunta, modifica, eliminazione)

        Parametri
        ----------
        :param mode : (string)
            Azione da eseguire (aggiunta, modifica o rimozione)
        :param voto : (string)
            Valore del voto in numero decimale.
        :param materia : (string)
            Materia relativa al voto.
        :param data : (string)
            Data relativa al voto.
        :param periodo : (string)
            Valore del parametro PERIODS delle impostazioni.
        :param tipo : (string)
            Tipo di voto.
        :param descrizione : (string)
            Descrizione del voto.
        :param peso : (string)
            Peso del voto.
        :param idx : (int)
            ID (indice) del voto


        Ritorna
        -------
        Niente
        """
    sql_conn = sql.connect(os.path.join(path, fn_voti), isolation_level=None)
    sql_cur = sql_conn.cursor()
    if mode in ["add", "del"]:
        sistemaIndici(sql_cur)
    try:
        if mode in ["add", "edit"]:
            for i in periodo.split(";"):
                if periodo.split(";").index(i) == 0:
                    continue
                k = i[1:].split(" - ")
                if k[0] < data < k[1]:
                    periodo = periodo.split(";").index(i)
                    break
        if peso == "":
            peso = "100"
        if "+" in voto:
            voto = str(float(voto[:-voto.count("+")]) + 0.25 * voto.count("+"))
        elif "-" in voto:
            voto = str(float(voto[:-voto.count("-")]) - 0.25 * voto.count("-"))
        if mode == "add":
            sql_cur.execute("INSERT INTO voti VALUES ('{}','{}','{}','{}', '{}','{}','{}','{}')".format(
                len(list(voti.keys())) + 1, voto, materia, data, periodo, tipo, peso, descrizione))
            wa.destroy()
        elif mode == "edit":
            sql_cur.execute(
                """UPDATE voti SET voto='{}', materia='{}', data='{}', periodo='{}', tipo='{}', peso='{}',
    descrizione='{}' WHERE ID={}""".format(voto, materia, data, periodo, tipo, peso, descrizione, idx))
            we.destroy()
        elif mode == "del":
            sql_cur.execute("DELETE FROM voti WHERE ID={}".format(idx))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wv.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore") + "\n" + str(
                           ex))
    if mode in ["add", "del"]:
        sistemaIndici(sql_cur)


def delete():
    """
        Avvisa l'utente che si sta per rimuovere un voto.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        • Niente
        """
    global selVoto
    selVoto = tv.item(tv.focus())
    if selVoto["text"] == "":
        tkmb.showwarning(title=_("Nessun voto selezionato!"),
                         message=_(
                             "Non è stato selezionato nessun voto. Si prega di selezionarne uno per apportare "
                             "modifiche."))
        return
    scelta = tkmb.askyesno(title=_("Conferma eliminazione"),
                           message=_("Si è sicuri di voler eliminare il voto {} nella materia {}?").format(
                               selVoto["values"][0], selVoto["values"][1]))
    if scelta is True:
        # noinspection PyTypeChecker
        Salvataggio("del", None, None, None, None, None, None, None, selVoto["text"])
    else:
        return


def edit():
    """
    Finestra per l'aggiunta del voto.

    Parametri
    ----------
    Nessuno

    Ritorna
    -------
    Niente
    """
    global selVoto
    selVoto = tv.item(tv.focus())
    if selVoto["text"] == "":
        tkmb.showwarning(title=_("Nessun voto selezionato!"),
                         message=_(
                             "Non è stato selezionato nessun voto. Si prega di selezionarne uno per apportare "
                             "modifiche."))
        return
    global we
    we = Toplevel()
    we.configure(background="white")
    we.title(_("Modifica voto") + " - School Life Diary")
    we.iconbitmap(r"images/school_life_diary.ico")
    we.geometry("450x350+600+200")
    fam = Labelframe(we, text=_("Maschera di inserimento"))
    fam.pack(padx=10, pady=10)
    lv = Label(fam, text=_("Voto"))
    lv.grid(row=0, column=0, padx=10, pady=10)
    vvar = StringVar(value=selVoto["values"][0])
    ev = Entry(fam, textvariable=vvar)
    ev.grid(row=0, column=1, padx=10, pady=10)
    lm = Label(fam, text=_("Materia"))
    lm.grid(row=1, column=0, padx=10, pady=10)
    em = Combobox(fam, postcommand=lambda: updatecombobox(em, False))
    em.grid(row=1, column=1, padx=10, pady=10)
    em.set(selVoto["values"][1])
    ld = Label(fam, text=_("Data"))
    ld.grid(row=2, column=0, padx=10, pady=10)
    dd = datepicker.Datepicker(fam)
    dd.grid(row=2, column=1, padx=10, pady=10)
    dd.date_var.set(selVoto["values"][2])
    setconn = sql.connect(os.path.join(path, "settings.db"), isolation_level=None)
    setc = setconn.cursor()
    setc.execute("SELECT * from settings WHERE setting='PERIODS'")
    periods = setc.fetchone()[1]
    lp = Label(fam, text=_("Tipo"))
    lp.grid(row=3, column=0, padx=10, pady=10)
    tc = Combobox(fam, values=[_("Scritto"), _("Orale"), _("Pratico"), _("Grafico"), _("Altro")])
    tc.grid(row=3, column=1, padx=10, pady=10)
    tc.set(selVoto["values"][4])
    lpeso = Label(fam, text=_("Peso"))
    lpeso.grid(row=4, column=0, padx=10, pady=10)
    var_peso = StringVar(value=selVoto["values"][5][:-1])
    e_peso = Entry(fam, textvariable=var_peso)
    e_peso.grid(row=4, column=1, padx=10, pady=10)
    ldescr = Label(fam, text=_("Descrizione"))
    ldescr.grid(row=5, column=0, padx=10, pady=10)
    var_descr = StringVar(value=selVoto["values"][6])
    e_descr = Entry(fam, textvariable=var_descr)
    e_descr.grid(row=5, column=1, padx=10, pady=10)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(we, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio("edit", vvar.get(), em.get(), dd.date_var.get(), periods, tc.get(),
                                           var_descr.get(), var_peso.get(), selVoto["text"]))
    b.pack(padx=10, pady=10)
    setc.close()
    setconn.close()
    we.mainloop()


def add():
    """
            Finestra per l'aggiunta del voto.

            Parametri
            ----------
            Nessuno

            Ritorna
            -------
            Niente
            """
    global wa
    wa = Toplevel()
    wa.configure(background="white")
    wa.title(_("Inserisci voto") + " - School Life Diary")
    wa.iconbitmap(r"images/school_life_diary.ico")
    wa.geometry("450x350+600+200")
    fam = Labelframe(wa, text=_("Maschera di inserimento"))
    fam.pack(padx=10, pady=10)
    lv = Label(fam, text=_("Voto"))
    lv.grid(row=0, column=0, padx=10, pady=10)
    vvar = StringVar(value="")
    ev = Entry(fam, textvariable=vvar)
    ev.grid(row=0, column=1, padx=10, pady=10)
    lm = Label(fam, text=_("Materia"))
    lm.grid(row=1, column=0, padx=10, pady=10)
    em = Combobox(fam, postcommand=lambda: updatecombobox(em, False))
    em.grid(row=1, column=1, padx=10, pady=10)
    ld = Label(fam, text=_("Data"))
    ld.grid(row=2, column=0, padx=10, pady=10)
    dd = datepicker.Datepicker(fam)
    dd.grid(row=2, column=1, padx=10, pady=10)
    setconn = sql.connect(os.path.join(path, "settings.db"), isolation_level=None)
    setc = setconn.cursor()
    setc.execute("SELECT * from settings WHERE setting='PERIODS'")
    periods = setc.fetchone()[1]
    lp = Label(fam, text=_("Tipo"))
    lp.grid(row=3, column=0, padx=10, pady=10)
    tc = Combobox(fam, values=[_("Scritto"), _("Orale"), _("Pratico"), _("Grafico"), _("Altro")])
    tc.grid(row=3, column=1, padx=10, pady=10)
    lpeso = Label(fam, text=_("Peso"))
    lpeso.grid(row=4, column=0, padx=10, pady=10)
    var_peso = StringVar(value="")
    e_peso = Entry(fam, textvariable=var_peso)
    e_peso.grid(row=4, column=1, padx=10, pady=10)
    ldescr = Label(fam, text=_("Descrizione"))
    ldescr.grid(row=5, column=0, padx=10, pady=10)
    var_descr = StringVar(value="")
    e_descr = Entry(fam, textvariable=var_descr)
    e_descr.grid(row=5, column=1, padx=10, pady=10)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(wa, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio("add", vvar.get(), em.get(), dd.date_var.get(), periods, tc.get(),
                                           var_descr.get(), var_peso.get()))
    b.pack(padx=10, pady=10)
    setc.close()
    setconn.close()
    wa.mainloop()


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
    global voti
    voti = {}
    cur.execute("SELECT * FROM voti")
    sr = cur.fetchall()
    for row in sr:
        voti[row[0]] = {"voto": row[1], "materia": row[2], "data": row[3], "periodo": row[4], "tipo": row[5],
                        "peso": row[6], "descrizione": row[7]}
    for r in voti:
        for i in voti[r]:
            if voti[r][i] is None:
                voti[r][i] = ""


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


def getmediapesata(d):
    """
    Calcola la media pesata dei voti visualizzati nella tabella.

    Parametri
    ----------
    :param d: (dict)
        Dizionario contenente tutti i voti della tabella

    Ritorna
    --------
    Media pesata
    """
    num = 0.0
    den = 0.0
    if d == {}:
        return _("Non è stato inserito nessun voto!")
    for x in list(d.keys()):
        num += (float(d[x]["voto"]) * float(d[x]["peso"]))
        den += float(d[x]["peso"])
    return num / den


def visualizzadati(cb):
    """
    Visualizza i voti nella tabella di una specifica materia selezionata dalla combobox

    Parametri
    ---------
    :param cb: (ttk.combobox)
        Combobox che contiene le materie come opzioni

    Ritorna
    --------
    Niente
    """
    tv.delete(*tv.get_children())
    if cb.get() == _("Tutte le materie"):
        cur.execute("SELECT * FROM voti")
    else:
        cur.execute("SELECT * FROM voti WHERE materia='{}'".format(cb.get()))
    votimat = {}
    sr = cur.fetchall()
    for row in sr:
        votimat[row[0]] = {"voto": row[1], "materia": row[2], "data": row[3], "periodo": row[4], "tipo": row[5],
                           "peso": row[6], "descrizione": row[7]}
    for r in votimat:
        for i in votimat[r]:
            if votimat[r][i] is None:
                votimat[r][i] = ""
    for x in list(votimat.keys()):
        tv.insert("", x, text=x, values=[votimat[x]["voto"],
                                         votimat[x]["materia"],
                                         votimat[x]["data"],
                                         votimat[x]["periodo"],
                                         votimat[x]["tipo"],
                                         str(votimat[x]["peso"]) + "%",
                                         votimat[x]["descrizione"]])
    media = getmediapesata(votimat)
    if isinstance(media, str):
        lmedia["text"] = _("MEDIA: {}").format(media)
    else:
        lmedia["text"] = _("MEDIA: {:.2f}").format(media)


def creaFinestra():
    """
        Crea la finestra dei voti.

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
    connection = sql.connect(os.path.join(path, fn_voti), isolation_level=None)
    global cur
    cur = connection.cursor()
    inizializza()
    wv.title(_("Voti") + " - School Life Diary")
    wv.iconbitmap(r"images/school_life_diary.ico")
    wv.geometry("1000x450+600+200")
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
    frame_materie = Labelframe(wv, text=_("Visualizzazione per materia"))
    frame_materie.pack(pady=10)
    cbm = Combobox(frame_materie, postcommand=lambda: updatecombobox(cbm))
    cbm.grid(row=0, column=0, padx=10, pady=10)
    cbm.set(_("Tutte le materie"))
    pview = PIL.Image.open(r"icons/search.png")
    iview = PIL.ImageTk.PhotoImage(pview)
    bv = Button(frame_materie, text=_("VISUALIZZA"), image=iview, compound=LEFT, command=lambda: visualizzadati(cbm))
    bv.grid(row=0, column=1, padx=10, pady=10)
    global tv
    tv = Treeview(wv)
    tv.pack(padx=10, pady=10)
    tv["columns"] = ("voto", "materia", "data", "periodo", "tipo", "peso", "descrizione")
    tv.heading("#0", text=_("ID"))
    tv.column("#0", width=50)
    tv.heading("voto", text=_("Voto"))
    tv.column("voto", width=75, anchor=CENTER)
    tv.heading("materia", text=_("Materia"))
    tv.column("materia", width=150, anchor=CENTER)
    tv.heading("data", text=_("Data"))
    tv.column("data", width=150, anchor=CENTER)
    tv.heading("periodo", text=_("Periodo"))
    tv.column("periodo", width=50, anchor=CENTER)
    tv.heading("tipo", text=_("Tipo"))
    tv.column("tipo", width=100, anchor=CENTER)
    tv.heading("peso", text=_("Peso"))
    tv.column("peso", width=60, anchor=CENTER)
    tv.heading("descrizione", text=_("Descrizione"))
    tv.column("descrizione", width=250, anchor=CENTER)
    tv.pack(padx=10, pady=10)
    tv.bind("<Double-Button-1>", lambda e: edit())
    tv.bind("<Button-3>", popup)
    for x in list(voti.keys()):
        tv.insert("", x, text=x, values=[voti[x]["voto"],
                                         voti[x]["materia"],
                                         voti[x]["data"],
                                         voti[x]["periodo"],
                                         voti[x]["tipo"],
                                         str(voti[x]["peso"]) + "%",
                                         voti[x]["descrizione"]])
    li = Label(wv, text=_(
        "Per aggiungere un voto, usa il tasto destro del mouse su uno spazio vuoto della finestra.\nPer "
        "modificare un voto, fai doppio click sulla riga corrispondente.\nPer modificare o eliminare un voto, "
        "selezionare una riga e poi premere il tasto destro del mouse."))
    li.pack()
    global lmedia
    media = getmediapesata(voti)
    setconn = sql.connect(os.path.join(path, "settings.db"), isolation_level=None)
    sc = setconn.cursor()
    if isinstance(media, str):
        lmedia = Label(wv, text=_("MEDIA: {}").format(media),
                       font=sc.execute("SELECT value FROM settings WHERE setting='PC_FONT'").fetchone()[0] + " bold")
    else:
        lmedia = Label(wv, text=_("MEDIA: {:.2f}").format(media),
                       font=sc.execute("SELECT value FROM settings WHERE setting='PC_FONT'").fetchone()[0] + " bold")
    if media != _("Non è stato inserito nessun voto!"):
        if float(media) < 5.50:
            lmedia.configure(foreground="red")
        elif 5.50 <= float(media) < 8:
            lmedia.configure(foreground="black")
        else:
            lmedia.configure(foreground="blue")
    lmedia.pack(pady=10)
    wv.bind("<Button-3>", popup2)
    wv.focus()
    conn.close()
    sc.close()
    setconn.close()
    wv.mainloop()
