# IMPORTAZIONE MODULI E LIBRERIE
import tkinter.messagebox as tkmb
from tkinter import *
from tkinter import Toplevel
from tkinter.colorchooser import askcolor
from tkinter.ttk import *

import PIL.Image
import PIL.ImageTk

from common import init
from common import variables

global path

module_name = __name__.replace("_", "")
if "." in module_name:
    module_name = module_name[module_name.find(".") + 1:]

path = variables.path

conn, c = init.connect_database()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subjects';")
ris = c.fetchall()
if not (len(ris) == 1):
    c.execute(
        """CREATE TABLE "subjects" ( `ID` INTEGER, `name` TEXT, `colour` TEXT, `prof` TEXT);""")
init.close_database(conn, c)


def inizializza():
    """
        Inizializzazione modulo materie:
            • Crea dizionario con tutte le materie, recuperate dal database

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    init.Language(module_name)
    global conn, c
    conn, c = init.connect_database()
    global m
    m = {}
    c.execute("SELECT * FROM subjects")
    sr = c.fetchall()
    for row in sr:
        m[row[0]] = {"nome": row[1], "colore": row[2], "prof": row[3]}
    for r in m:
        for i in m[r]:
            if m[r][i] is None:
                m[r][i] = ""


def sistemaIndici():
    """
        Corregge possibili negli indici delle materie, salvate nel database.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
            """
    c.execute("SELECT * FROM subjects")
    r = c.fetchall()
    for i in range(len(r)):
        if i in r[i]:
            continue
        else:
            c.execute("""UPDATE subjects SET ID={} WHERE name='{}' AND colour='{}'
            AND prof='{}'""".format(i + 1, r[i][1], r[i][2], r[i][3]))


def Salvataggio(mode, name, col, prof, idx=0):
    """
        Salva la materia nel database, in base all'azione scelta (aggiunta, modifica, eliminazione)

        Parametri
        ----------
        :param mode : (string)
            Azione da eseguire (aggiunta, modifica o rimozione)
        :param name : (string)
            Nome della materia.
        :param col : (string)
            Colore della materia.
        :param prof : (string)
            Professore relativo alla materia.
        :param idx : (int)
            ID (indice) della materia


        Ritorna
        -------
        Niente
        """
    sistemaIndici()
    try:
        if mode == "add":
            c.execute(
                "INSERT INTO subjects VALUES ('{}','{}','{}','{}')".format(len(list(m.keys())) + 1, name, col, prof))
            wa.destroy()
        elif mode == "edit":
            c.execute(
                """UPDATE subjects SET name='{}', colour='{}', prof='{}' WHERE ID={}""".format(name, col, prof, idx))
            we.destroy()
        elif mode == "del":
            c.execute("DELETE FROM subjects WHERE ID={}".format(idx))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Salvataggio effettuato con successo!"))
        wim.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_("Si è verificato un errore, riprovare oppure contattare lo sviluppatore") + "\n" + str(
                           ex))
    sistemaIndici()


def delete():
    """
        Avvisa l'utente che si sta per rimuovere una materia.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        • Niente
        """
    global selMat
    selMat = tm.item(tm.focus())
    if selMat["text"] == "":
        tkmb.showwarning(title=_("Nessuna materia selezionata!"),
                         message=_(
                             "Non è stata selezionata nessuna materia. Si prega di selezionarne una per apportare "
                             "modifiche."))
        return
    scelta = tkmb.askyesno(title=_("Conferma eliminazione"),
                           message=_("Si è sicuri di voler eliminare la materia {} ?").format(selMat["values"][0]))
    if scelta is True:
        Salvataggio("del", None, None, None, selMat["text"])
    else:
        return


def scegliColore(cc):
    """
        Color Picker. Scegli colore.

        Parametri
        ----------
        :param cc : (Tkinter Canvas)
            Widget canvas

        Ritorna
        -------
        Niente
        """
    color = askcolor()
    cc["background"] = color[1]


def updatecb(cb, l):
    """
        Aggiornamento opzioni menu a tendina con la lista dei professori

        Parametri
        ----------
        :param cb : (Tkinter Combobox)
            Menu a tendina vuoto
        :param l : (list)
            Lista professori

        Ritorna
        -------
        Niente
        """
    lp = []
    for i in l:
        lp.append("{} {}".format(i[1], i[2]))
    cb["values"] = lp


def add():
    """
        Finestra per l'aggiunta della materia.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    global wa
    wa = Toplevel()
    variables.change_window_bg(wa)
    wa.title(_("Inserisci materia") + " - School Life Diary")
    wa.iconbitmap(r"images/school_life_diary.ico")
    wa.geometry("350x300+600+200")
    fam = Labelframe(wa, text=_("Maschera di inserimento"))
    fam.pack(padx=10, pady=10)
    l = Label(fam, text=_("Materia"))
    l.grid(row=0, column=0, padx=10, pady=10)
    var = StringVar(value="")
    e = Entry(fam, textvariable=var)
    e.grid(row=0, column=1, padx=10, pady=10)
    lc = Label(fam, text=_("Colore"))
    cc = Canvas(fam, bg="light blue", width=50, height=20)
    cc.bind("<Button-1>", lambda event: scegliColore(cc))
    lc.grid(row=2, column=0, padx=1, pady=5)
    cc.grid(row=2, column=1, padx=1, pady=5)
    lp = Label(fam, text=_("Professore"))
    lp.grid(row=3, column=0, padx=1, pady=5)
    ep = Combobox(fam)
    ep.grid(row=3, column=1, padx=1, pady=5)
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prof';")
    result = c.fetchall()
    if len(result) == 1:
        c.execute("SELECT * FROM prof")
        listaprof = c.fetchall()
        updatecb(ep, listaprof)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(wa, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio("add", var.get(), cc["background"], ep.get()))
    b.pack(padx=10, pady=10)
    wa.mainloop()


def edit():
    """
        Modifica la materia.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        • Niente
        """
    global selMat
    selMat = tm.item(tm.focus())
    if selMat["text"] == "":
        tkmb.showwarning(title=_("Nessuna materia selezionata!"),
                         message=_(
                             "Non è stata selezionata nessuna materia. Si prega di selezionarne una per apportare "
                             "modifiche."))
        return
    global we
    we = Toplevel()
    variables.change_window_bg(we)
    we.title(_("Modifica materia") + " - School Life Diary")
    we.iconbitmap(r"images/school_life_diary.ico")
    we.geometry("350x300+600+200")
    fam = Labelframe(we, text=_("Maschera di modifica"))
    fam.pack(padx=10, pady=10)
    l = Label(fam, text=_("Materia"))
    l.grid(row=0, column=0, padx=10, pady=10)
    var = StringVar(value=selMat["values"][0])
    e = Entry(fam, textvariable=var)
    e.grid(row=0, column=1, padx=10, pady=10)
    lc = Label(fam, text=_("Colore"))
    cc = Canvas(fam, bg=selMat["values"][1], width=50, height=20)
    cc.bind("<Button-1>", lambda event: scegliColore(cc))
    lc.grid(row=2, column=0, padx=1, pady=5)
    cc.grid(row=2, column=1, padx=1, pady=5)
    lp = Label(fam, text=_("Professore"))
    lp.grid(row=3, column=0, padx=1, pady=5)
    ep = Combobox(fam, )
    ep.grid(row=3, column=1, padx=1, pady=5)
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prof';")
    result = c.fetchall()
    if len(result) == 1:
        c.execute("SELECT * FROM prof")
        listaprof = c.fetchall()
        updatecb(ep, listaprof)
    ep.set(selMat["values"][2])
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(we, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio("edit", var.get(), cc["background"], ep.get(), selMat["text"]))
    b.pack(padx=10, pady=10)
    we.mainloop()


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
    if event.widget != tm:
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
    if event.widget != wim:
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
    global wim
    wim = Toplevel()
    variables.change_window_bg(wim)
    inizializza()
    wim.title(_("Materie") + " - School Life Diary")
    wim.iconbitmap(r"images/school_life_diary.ico")
    wim.geometry("750x375+600+200")
    i_add = PhotoImage(file=r"icons/add.png")
    i_edit = PhotoImage(file=r"icons/edit.png")
    i_del = PhotoImage(file=r"icons/delete.png")
    global aMenu
    aMenu = Menu(wim, tearoff=0)
    aMenu.add_command(label=_('Aggiungi'), image=i_add, compound="left",
                      command=add)
    aMenu.add_command(label=_('Modifica'), image=i_edit, compound="left",
                      command=edit)
    aMenu.add_command(label=_('Elimina'), image=i_del, compound="left",
                      command=delete)
    global bMenu
    bMenu = Menu(wim, tearoff=0)
    bMenu.add_command(label=_('Aggiungi'), image=i_add, compound="left",
                      command=add)
    global tm
    tm = Treeview(wim)
    tm.pack(padx=10, pady=10)
    tm["columns"] = ("nome", "colore", "prof")
    tm.heading("#0", text=_("ID"))
    tm.column("#0", width=50)
    tm.heading("nome", text=_("Nome Materia"))
    tm.column("nome", anchor=CENTER)
    tm.heading("colore", text=_("Colore Materia"))
    tm.column("colore", anchor=CENTER)
    tm.heading("prof", text=_("Professore"))
    tm.column("prof", anchor=CENTER)
    tm.pack(padx=10, pady=10)
    tm.bind("<Double-Button-1>", lambda e: edit())
    tm.bind("<Button-3>", popup)
    for x in list(m.keys()):
        tm.insert("", x, text=x, values=[m[x]["nome"],
                                         m[x]["colore"],
                                         m[x]["prof"]])
    li = Label(wim, text=_(
        "Per aggiungere una materia, usa il tasto destro del mouse su uno spazio vuoto della finestra.\nPer "
        "modificare una materia, fai doppio click sulla riga corrispondente.\nPer modificare o eliminare una materia, "
        "selezionare una riga e poi premere il tasto destro del mouse."))
    li.pack()
    wim.bind("<Button-3>", popup2)
    wim.focus()
    wim.mainloop()
