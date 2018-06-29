import sys

### IMPOSTAZIONE PERCORSO LIBRERIE ESTERNE ###
sys.path.insert(0, 'lib')

import ctypes
import gettext
import locale
import os
import os.path
import time
import sqlite3 as sql
from tkinter import *
from tkinter import Toplevel
from tkinter.scrolledtext import *
from tkinter.ttk import *
import tkinter.messagebox as tkmb
import tk_tools as tkt
import datepicker
import PIL.Image
import PIL.ImageTk

global ag

ag = {}
'''
AG è un dizionario con la seguente struttura (rappresenta una tabella): ag={"anno":{"mese":{"idevento":{"data": "xxx",
"tipo": "valoretipo", "titolo":"valoretitolo","descrizione":"valoredescr", "materia":"valoremateria", "tipo_evento":
 "interrogazione/verifica", "allegati":"percorsoallegati"...}}, ...}
'''

global fn_agenda
global path
fn_agenda = "agenda.db"

path = os.path.expanduser(r'~\Documents\School Life Diary')
if not (os.path.exists(os.path.join(path, fn_agenda))):
    fm = open(os.path.join(path, fn_agenda), "w")
    fm.close()


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
        lg = gettext.translation("agenda", localedir=os.path.join(path, 'locale'), languages=[lgcode])
    else:
        fl = open(os.path.join(path, "language.txt"), "r")
        lgcode = fl.readline()
        lg = gettext.translation('agenda', localedir=os.path.join(path, 'locale'), languages=[lgcode])
    lg.install()
    locale.setlocale(locale.LC_ALL, lgcode)


def sistemaIndici(cursor):
    """
        Corregge possibili errori negli indici degli eventi, salvati nel database.

        Parametri
        ----------
        :param cursor : (sqlite3.Cursor)
            Cursore che effettua operazioni sul database.

        Ritorna
        -------
        Niente
            """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = cursor.fetchall()
    for table in result:
        for x in table:
            if x == "sqlite_sequence":
                continue
            cursor.execute("SELECT * FROM `{}`".format(x))
            r = cursor.fetchall()
            for i in range(len(r)):
                if i in r[i]:
                    continue
                else:
                    cursor.execute("""UPDATE `{}` SET ID={} WHERE data='{}' AND tipo='{}'
                    AND titolo='{}' AND descrizione='{}' AND materia='{}' AND tipo_verifica='{}'
                    AND allegati='{}'""".format(x, i + 1, r[i][1], r[i][2], r[i][3], r[i][4], r[i][5], r[i][6], r[i][7])
                                   )


def Salvataggio(mode, titolo, descrizione, data, tipo, tipo_v, materia, idx=0):
    """
        Salva l'evento nel database, in base all'azione scelta (aggiunta, modifica, eliminazione)

        Parametri
        ----------
        :param mode : (string)
            Azione da eseguire (aggiunta, modifica o rimozione)
        :param titolo : (string)
            Titolo dell'evento
        :param descrizione : (string)
            Descrizione dell'evento.
        :param data : (string)
            Data dell'evento.
        :param tipo : (string)
            Tipo dell'evento.
        :param tipo_v : (string)
            Tipo della verifica (se è stato selezionato "Verifica" come tipo evento)
        :param materia : (string)
            Materia relativa all'evento.
        :param idx : (int)
            ID (indice) dell'evento


        Ritorna
        -------
        Niente
        """
    if data == "":
        tkmb.showerror(_("Nessuna data inserita!"), _("Per proseguire è necessario inserire una data."))
        return
    sql_conn = sql.connect(os.path.join(path, fn_agenda), isolation_level=None)
    sql_cur = sql_conn.cursor()
    if mode in ["add", "del"]:
        sistemaIndici(sql_cur)
    try:
        d_s = data.split("-")
        table_name = "{}_{}".format(d_s[0], d_s[1])
        sql_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = sql_cur.fetchall()
        table_list = []
        for i in res:
            for a in i:
                if a == "sqlite_sequence":
                    continue
                table_list.append(a)
        if not (table_name in table_list):
            sql_cur.execute("""CREATE TABLE `{}` (
        `ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        `data`	TEXT,
        `tipo`	TEXT,
        `titolo`	TEXT,
        `descrizione`	TEXT,
        `materia`	TEXT,
        `tipo_verifica`	TEXT,
        `allegati`	TEXT
    );""".format(table_name))
        if mode == "add":
            if "sf" in globals():
                sql_cur.execute("INSERT INTO `{}` VALUES ('{}','{}','{}','{}', '{}','{}','{}','{}')".format(
                    table_name, len(list(ag.keys())) + 1, data, tipo, titolo, descrizione, materia, tipo_v, sf))
            else:
                sql_cur.execute("INSERT INTO `{}` VALUES ('{}','{}','{}','{}', '{}','{}','{}','{}')".format(
                    table_name, len(list(ag.keys())) + 1, data, tipo, titolo, descrizione, materia, tipo_v, ""))
            wa.destroy()
        elif mode == "edit":
            if "sf" in globals():
                sql_cur.execute("""UPDATE `{}` SET data='{}', tipo='{}', titolo='{}', descrizione='{}', materia='{}',
        tipo_v='{}', allegati='{}' WHERE ID={}""".format(table_name, data, tipo, titolo, descrizione, materia,
                                                         tipo_v, sf, idx))
            else:
                sql_cur.execute("""UPDATE `{}` SET data='{}', tipo='{}', titolo='{}', descrizione='{}', materia='{}',
                        tipo_v='{}' WHERE ID={}""".format(table_name, data, tipo, titolo, descrizione, materia, tipo_v,
                                                          idx))
            we.destroy()
        elif mode == "del":
            sql_cur.execute("DELETE FROM `{}` WHERE ID={}".format(table_name, idx))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        aw.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore") + "\n" + str(
                           ex))
    if mode in ["add", "del"]:
        sistemaIndici(sql_cur)


def delete():
    """
        Avvisa l'utente che si sta per rimuovere un evento.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        • Niente
        """
    global sel
    sel = tc.item(tc.focus())
    if sel["text"] == "":
        tkmb.showwarning(title=_("Nessun voto selezionato!"),
                         message=_(
                             "Non è stato selezionato nessun evento. Si prega di selezionarne uno per apportare "
                             "modifiche."))
        return
    scelta = tkmb.askyesno(title=_("Conferma eliminazione"),
                           message=_("Si è sicuri di voler eliminare l'evento con titolo {}, collegato alla materia "
                                     "{}?").format(sel["values"][1], sel["values"][4]))
    if scelta is True:
        # noinspection PyTypeChecker
        Salvataggio("del", None, None, None, None, None, None, sel["text"])
    else:
        return


def selezionecombobox(l, cb, selezione):
    """
    Rende visibile il campo "Tipo Verifica"

    Parametri
    ----------
    :param l: (tkinter.Label)
        Etichetta del campo "Tipo Verifica"
    :param cb: (ttk.Combobox)
        Combobox del campo "Tipo Verifica"
    :param selezione: (string)
        Selezione dalla combobox

    Ritorna
    --------
    Niente
    """
    if selezione == _("Verifica"):
        l.grid(row=4, column=0, padx=10, pady=5)
        cb.grid(row=4, column=1, padx=10, pady=2)
    else:
        l.grid_forget()
        cb.grid_forget()


def file(lf):
    """
        Apre il file picker

        Parametri
        ----------
        :param lf : (Label)
            Parametro che identifica l'etichetta con il nome del file.

        Ritorna
        -------
        Niente
        """
    global sf
    sf = filedialog.askopenfilename()
    global fs
    fs = sf.split("/")
    if fs[len(fs) - 1] != "":
        lf["text"] = fs[len(fs) - 1]


def edit():
    """
    Finestra per la modifica dell'evento.

    Parametri
    ----------
    Nessuno

    Ritorna
    -------
    Niente
    """
    global sel
    sel = tc.item(tc.focus())
    if sel["text"] == "":
        tkmb.showwarning(title=_("Nessun evento selezionato"),
                         message=_("Non è stato selezionato nessun evento. "
                                   "Si prega di selezionarne uno per apportarne le modifiche."))
        return
    global we
    we = Toplevel()
    we.configure(bg="white")
    we.title(_("Modifica evento") + " - School Life Diary")
    we.iconbitmap(r"images/school_life_diary.ico")
    we.geometry("700x450+600+200")
    f = LabelFrame(we, text=_("Maschera di modifica"))
    f.pack()
    l = Label(f, text=_("Titolo"))
    l.grid(row=0, column=0, padx=10, pady=5)
    vart = StringVar(value=sel["values"][2])
    et = Entry(f, textvariable=vart, width=50)
    et.grid(row=0, column=1, padx=10, pady=2)
    l1 = Label(f, text=_("Descrizione"))
    l1.grid(row=1, column=0, padx=10, pady=5)
    ec = ScrolledText(f, width=50, height=10)
    ec.insert(INSERT, sel["values"][3])
    ec.grid(row=1, column=1, padx=10, pady=2)
    ld = Label(f, text=_("Data"))
    ld.grid(row=2, column=0, padx=10, pady=5)
    dd = datepicker.Datepicker(f)
    dd.grid(row=2, column=1, padx=10, pady=2)
    dd.date_var.set(sel["values"][0])
    l111 = Label(f, text=_("Tipo verifica"))
    cbtv = Combobox(f, values=[_("Verifica scritta"), _("Interrogazione")])
    cbtv.set(sel["values"][5])
    l11 = Label(f, text=_("Tipo evento"))
    l11.grid(row=3, column=0, padx=10, pady=5)
    cbt = Combobox(f, values=[_("Promemoria"), _("Verifica"), _("Compito")])
    cbt.grid(row=3, column=1, padx=10, pady=5)
    cbt.set(sel["values"][1])
    cbt.bind("<<ComboboxSelected>>", lambda e: selezionecombobox(l111, cbtv, cbt.get()))
    l12 = Label(f, text=_("Materia"))
    l12.grid(row=5, column=0, padx=10, pady=5)
    matconn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
    matc = matconn.cursor()
    matc.execute("SELECT * FROM subjects")
    r = matc.fetchall()
    listamat = []
    if not (r == []):
        for i in r:
            listamat.append(i[1])
    cbe = Combobox(f, values=listamat)
    cbe.grid(row=5, column=1, padx=10, pady=5)
    cbe.set(sel["values"][4])
    l2 = Label(f, text=_("Allegato (opzionale)"))
    l2.grid(row=6, column=0, padx=10, pady=5)
    fa = Frame(f)
    fa.grid(row=6, column=1)
    lf = Label(fa, text=_("Nessun file selezionato"))
    if len(sel["values"]) < 6:
        lf["text"] = sel["values"][6][sel["values"][6].rfind("/") + 1:]
    idx = sel["text"]
    data = sel["values"][0]
    datasp = data.split("-")
    global sf
    sf = ag["{}_{}".format(datasp[0], datasp[1])][datasp[1]][idx]["allegati"]
    pfile = PIL.Image.open(r"icons/pick_file.png")
    ifile = PIL.ImageTk.PhotoImage(pfile)
    btn = Button(fa, text=_("SCEGLI FILE"), image=ifile, compound=LEFT, command=lambda: file(lf))
    btn.grid(row=0, column=0, padx=10, pady=2)
    lf.grid(row=0, column=1, padx=10, pady=2)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(we, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: Salvataggio("add", vart.get(),
                                                                                            ec.get(1.0, END), dd.get(),
                                                                                            cbt.get(), cbtv.get(),
                                                                                            cbe.get()))
    b.pack(padx=10, pady=10)
    we.mainloop()


def add():
    """
    Finestra per l'aggiunta dell'evento.

    Parametri
    ----------
    Nessuno

    Ritorna
    -------
    Niente
    """
    global wa
    wa = Toplevel()
    wa.configure(bg="white")
    wa.title(_("Inserisci evento") + " - School Life Diary")
    wa.iconbitmap(r"images/school_life_diary.ico")
    wa.geometry("700x450+600+200")
    f = LabelFrame(wa, text=_("Maschera di inserimento"))
    f.pack()
    l = Label(f, text=_("Titolo"))
    l.grid(row=0, column=0, padx=10, pady=5)
    vart = StringVar(value="")
    et = Entry(f, textvariable=vart, width=50)
    et.grid(row=0, column=1, padx=10, pady=2)
    l1 = Label(f, text=_("Descrizione"))
    l1.grid(row=1, column=0, padx=10, pady=5)
    ec = ScrolledText(f, width=50, height=10)
    ec.grid(row=1, column=1, padx=10, pady=2)
    ld = Label(f, text=_("Data"))
    ld.grid(row=2, column=0, padx=10, pady=5)
    dd = datepicker.Datepicker(f)
    dd.grid(row=2, column=1, padx=10, pady=2)
    if cal.selection is not None:
        dd.date_var.set(cal.selection)
    l111 = Label(f, text=_("Tipo Verifica"))
    cbtv = Combobox(f, values=[_("Verifica scritta"), _("Interrogazione")])
    l11 = Label(f, text=_("Tipo evento"))
    l11.grid(row=3, column=0, padx=10, pady=5)
    cbt = Combobox(f, values=[_("Promemoria"), _("Verifica"), _("Compito")])
    cbt.grid(row=3, column=1, padx=10, pady=5)
    cbt.bind("<<ComboboxSelected>>", lambda e: selezionecombobox(l111, cbtv, cbt.get()))
    l12 = Label(f, text=_("Materia"))
    l12.grid(row=5, column=0, padx=10, pady=5)
    matconn = sql.connect(os.path.join(path, "subjects.db"), isolation_level=None)
    matc = matconn.cursor()
    matc.execute("SELECT * FROM subjects")
    r = matc.fetchall()
    listamat = []
    if not (r == []):
        for i in r:
            listamat.append(i[1])
    cbe = Combobox(f, values=listamat)
    cbe.grid(row=5, column=1, padx=10, pady=5)
    l2 = Label(f, text=_("Allegato (opzionale)"))
    l2.grid(row=6, column=0, padx=10, pady=5)
    fa = Frame(f)
    fa.grid(row=6, column=1)
    lf = Label(fa, text=_("Nessun file selezionato"))
    pfile = PIL.Image.open(r"icons/pick_file.png")
    ifile = PIL.ImageTk.PhotoImage(pfile)
    btn = Button(fa, text=_("SCEGLI FILE"), image=ifile, compound=LEFT, command=lambda: file(lf))
    btn.grid(row=0, column=0, padx=10, pady=2)
    lf.grid(row=0, column=1, padx=10, pady=2)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(wa, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: Salvataggio("add", vart.get(),
                                                                                            ec.get(1.0, END), dd.get(),
                                                                                            cbt.get(), cbtv.get(),
                                                                                            cbe.get()))
    b.pack(padx=10, pady=10)
    wa.mainloop()


def inizializza(c):
    """
    Inizializzazione modulo agenda:
        • Crea dizionario con tutti gli eventi, recuperati dal database

    Parametri
    ----------
    :param c: (sql connection)
        Connessione al database SQLite

    Ritorna
    -------
    :return False: (bool)
        Se il database è vuoto
    :return True: (bool)
        Se il database è pieno
    """
    install_language()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    r = c.fetchall()
    if r == []:
        return False
    else:
        global ag
        ag = {}
        for a in r:
            year = {}
            for y in a:
                if y == "sqlite_sequence":
                    continue
                c.execute("SELECT * FROM `{}`".format(y))
                res = c.fetchall()
                y_m = y.split("_")
                month = {}
                for row in res:
                    month[row[0]] = {"data": row[1], "tipo": row[2], "titolo": row[3], "descrizione": row[4],
                                     "materia": row[5], "tipo_verifica": row[6], "allegati": row[7]}
                year[y_m[1]] = month
            ag[a[0]] = year
        return True


def visualizzadati(cba, cbm):
    """
    Visualizza gli eventi di un specifico mese selezionato dalla combobox nella tabella

    Parametri
    ---------
    :param cba: (ttk.combobox)
        Combobox che contiene gli anni come opzioni

    :param cbm: (ttk.combobox)
        Combobox che contiene i mesi come opzioni

    Ritorna
    --------
    Niente
    """
    tc.delete(*tc.get_children())
    months = ["", _("Gennaio"), _("Febbraio"), _("Marzo"), _("Aprile"), _("Maggio"), _("Giugno"), _("Luglio"),
              _("Agosto"), _("Settembre"), _("Ottobre"), _("Novembre"), _("Dicembre")]
    eventimese = {}
    if cbm.get() == _("Tutto l'anno"):
        for i in ag.keys():
            if cba.get() in i:
                eventimese[i] = ag[i]
    else:
        for i in ag.keys():
            monthid = str(months.index(cbm.get()))
            if len(monthid) == 1:
                monthid = "0" + monthid
            if i == "{}_{}".format(cba.get(), monthid):
                eventimese[i] = ag[i]
    patt = PIL.Image.open(r"icons/paper-clip.png")
    iatt = PIL.ImageTk.PhotoImage(patt)
    for i in eventimese.keys():
        for k in eventimese[i].keys():
            for x in eventimese[i][k].keys():
                if eventimese[i][k][x]["allegati"] == "":
                    tc.insert("", x, text=x, values=[eventimese[i][k][x]["data"],
                                                     eventimese[i][k][x]["tipo"],
                                                     eventimese[i][k][x]["titolo"],
                                                     eventimese[i][k][x]["descrizione"],
                                                     eventimese[i][k][x]["materia"],
                                                     eventimese[i][k][x]["tipo_verifica"]])
                else:
                    tc.insert("", x, text=x, values=[eventimese[i][k][x]["data"],
                                                     eventimese[i][k][x]["tipo"],
                                                     eventimese[i][k][x]["titolo"],
                                                     eventimese[i][k][x]["descrizione"],
                                                     eventimese[i][k][x]["materia"],
                                                     eventimese[i][k][x]["tipo_verifica"],
                                                     eventimese[i][k][x]["allegati"][
                                                     eventimese[i][k][x]["allegati"].rfind("/") + 1:
                                                     ]],
                              image=iatt)


def on_double_click(event):
    """
        Apri l'allegato della annotazione

        Parametri
        ----------
        :param event : (treeview callback)
            Parametro che identifica l'evento del cliccare due volte una annotazione dalla tabella.

        Ritorna
        -------
        Niente
        """
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    idx = item["text"]
    data = item["values"][0]
    datasp = data.split("-")
    url = ag["{}_{}".format(datasp[0], datasp[1])][datasp[1]][idx]["allegati"]
    os.startfile(url)


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
    if event.widget != tc:
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
    if not (event.widget == aw):
        return
    # display the popup menu
    try:
        bMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        bMenu.grab_release()


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
    global es
    es = inizializza(c)
    global aw
    aw = Toplevel()
    aw.title(_("Agenda - School Life Diary"))
    aw.configure(bg="white")
    aw.iconbitmap(r"images/school_life_diary.ico")
    i_add = PhotoImage(file=r"icons/add.png")
    global bMenu
    bMenu = Menu(aw, tearoff=0)
    bMenu.add_command(label=_('Aggiungi'), image=i_add, compound="left",
                      command=add)
    global cal
    cal = tkt.Calendar(aw)
    cal.pack()
    cal.add_callback(add)
    aw.bind("<Button-3>", popup2)
    if not (es is False):
        aw.geometry("1250x600+200+200")
        i_edit = PhotoImage(file=r"icons/edit.png")
        i_del = PhotoImage(file=r"icons/delete.png")
        patt = PIL.Image.open(r"icons/paper-clip.png")
        iatt = PIL.ImageTk.PhotoImage(patt)
        global aMenu
        aMenu = Menu(aw, tearoff=0)
        aMenu.add_command(label=_('Aggiungi'), image=i_add, compound="left",
                          command=add)
        aMenu.add_command(label=_('Modifica'), image=i_edit, compound="left",
                          command=edit)
        aMenu.add_command(label=_('Elimina'), image=i_del, compound="left", command=delete)
        aMenu.add_separator()
        months = ["", _("Gennaio"), _("Febbraio"), _("Marzo"), _("Aprile"), _("Maggio"), _("Giugno"), _("Luglio"),
                  _("Agosto"), _("Settembre"), _("Ottobre"), _("Novembre"), _("Dicembre")]
        currentmonth = time.strftime("%m")
        currentyear = time.strftime("%Y")
        fcb = Labelframe(aw, text=_("Visualizzazione per mese"))
        fcb.pack(padx=10, pady=10)
        cba = Combobox(fcb, text=currentyear, values=list(reversed(range(2000, int(currentyear) + 6))))
        cba.grid(row=0, column=0, padx=2, pady=2)
        cbm = Combobox(fcb, text=months[int(currentmonth)], values=[_("Tutto l'anno")] + months[1:])
        cbm.grid(row=0, column=1, padx=2, pady=2)
        pview = PIL.Image.open(r"icons/search.png")
        iview = PIL.ImageTk.PhotoImage(pview)
        bv = Button(fcb, text=_("VISUALIZZA"), image=iview, compound=LEFT,
                    command=lambda: visualizzadati(cba, cbm))
        bv.grid(row=0, column=2, padx=10, pady=10)
        global tc
        tc = Treeview(aw)
        tc["columns"] = ("data", "tipo", "titolo", "descrizione", "materia", "tipo_verifica", "allegati")
        tc.heading("#0", text=_("ID"))
        tc.column("#0", width=50)
        tc.heading("data", text=_("Data"))
        tc.column("data", width=150)
        tc.heading("tipo", text=_("Tipo"))
        tc.column("tipo", width=150)
        tc.heading("titolo", text=_("Titolo"))
        tc.column("titolo", width=200)
        tc.heading("descrizione", text=_("Descrizione"))
        tc.heading("materia", text=_("Materia"))
        tc.column("materia", width=150)
        tc.heading("tipo_verifica", text=_("Tipo verifica"))
        tc.column("tipo_verifica", width=150)
        tc.heading("allegati", text=_("Allegati"))
        tc.column("allegati", width=125)
        for i in ag.keys():
            for k in ag[i].keys():
                for x in ag[i][k].keys():
                    if ag[i][k][x]["allegati"] == "":
                        tc.insert("", x, text=x, values=[ag[i][k][x]["data"],
                                                         ag[i][k][x]["tipo"],
                                                         ag[i][k][x]["titolo"],
                                                         ag[i][k][x]["descrizione"],
                                                         ag[i][k][x]["materia"],
                                                         ag[i][k][x]["tipo_verifica"]])
                    else:
                        tc.insert("", x, text=x, values=[ag[i][k][x]["data"],
                                                         ag[i][k][x]["tipo"],
                                                         ag[i][k][x]["titolo"],
                                                         ag[i][k][x]["descrizione"],
                                                         ag[i][k][x]["materia"],
                                                         ag[i][k][x]["tipo_verifica"],
                                                         ag[i][k][x]["allegati"][
                                                         ag[i][k][x]["allegati"].rfind("/") + 1:
                                                         ]],
                                  image=iatt)

        tc.pack(padx=10, pady=10)
        tc.bind("<Double-Button-1>", on_double_click)
        tc.bind("<Button-3>", popup)
        li = Label(aw, text=_("Per aggiungere un evento occorre premere con il tasto destro o su uno spazio vuoto "
                              "della finestra e premere Aggiungi.\n"
                              "Per modificare un evento clicca con il tasto destro su un evento nella tabella e"
                              "seleziona Modifica.\n"
                              "Per eliminare un evento clicca con il tasto destro su un evento nella tabella e"
                              "seleziona Elimina."))
    else:
        aw.geometry("750x325+250+200")
        l = Label(aw, text=_("Nessun evento è stato pianificato."))
        l.pack(pady=10)
        li = Label(aw, text=_("Per aggiungere un evento occorre premere con il tasto destro su uno spazio vuoto della "
                              "finestra e premere Aggiungi."))
    li.pack(pady=2)
    aw.bind("<Button-3>", popup2)
    aw.mainloop()
