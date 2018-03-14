# IMPORTAZIONE MODULI E LIBRERIE
import PIL.Image
import PIL.ImageTk
import ctypes
import gettext
import locale
import os.path
import sqlite3 as sql
import webbrowser
from tkinter.filedialog import askopenfilename

global fn_prof
global path

fn_prof = "prof.db"

path = os.path.expanduser(r'~\Documents\School Life Diary')
if not (os.path.exists(os.path.join(path, fn_prof))):
    fm = open(os.path.join(path, fn_prof), "w")
    fm.close()
    conn = sql.connect(os.path.join(path, fn_prof), isolation_level=None)
    c = conn.cursor()
    c.execute("""CREATE TABLE `prof` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`nome`	TEXT,
	`cognome`	TEXT NOT NULL,
	`imageURI`	TEXT,
	`web`	TEXT,
	`email`	TEXT
);""")
else:
    conn = sql.connect(os.path.join(path, fn_prof), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prof';")
    ris = c.fetchall()
    if not (len(ris) == 1):
        c.execute("""CREATE TABLE `prof` (
            `ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            `nome`	TEXT,
            `cognome`	TEXT NOT NULL,
            `imageURI`	TEXT,
            `web`	TEXT,
            `email`	TEXT
    );""")

# INSTALLAZIONE LINGUA
if not (os.path.exists(os.path.join(path, "language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl = ["en", "it"]
    lg = gettext.translation("subjects", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
else:
    fl = open(os.path.join(path, "language.txt"), "r")
    lgcode = fl.readline()
    lg = gettext.translation('subjects', localedir=os.path.join(path, 'locale'), languages=[lgcode])
lg.install()

# IMPORTAZIONE LIBRERIE PER LA GRAFICA
from tkinter import *
import tkinter.messagebox as tkmb
from tkinter.ttk import *
from tkinter import Toplevel


# INIZIALIZZA DATI
def inizializza():
    global prof
    prof = {}
    conn = sql.connect(os.path.join(path, fn_prof), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM prof")
    sr = c.fetchall()
    for row in sr:
        prof[row[0]] = {"nome": row[1], "cognome": row[2], "imageURI": row[3], "web": row[4], "email": row[5]}
    for r in prof:
        for i in prof[r]:
            if prof[r][i] == None:
                prof[r][i] = ""
    c.close()


def sistemaIndici(conn, c):
    c.execute("SELECT * FROM prof")
    r = c.fetchall()
    for i in range(len(r)):
        if i in r[i]:
            continue
        else:
            c.execute("""UPDATE prof SET ID={} WHERE nome='{}' AND cognome='{}'
            AND imageURI='{}' AND web='{}' AND email='{}'""".format(i + 1, r[i][1], r[i][2], r[i][3], r[i][4], r[i][5]))


def Salvataggio(mode, nome=None, cognome=None, sitoweb=None, email=None, idx=0):
    try:
        conn = sql.connect(os.path.join(path, fn_prof), isolation_level=None)
        c = conn.cursor()
        sistemaIndici(conn, c)
        if mode == "add":
            c.execute("SELECT * FROM prof")
            r = c.fetchall()
            if "fImage" in globals() and not (fImage == None):
                c.execute(
                    "INSERT INTO prof VALUES ('{}','{}','{}','{}','{}','{}')".format(len(prof.keys()) + 1, nome.get(),
                                                                                     cognome.get(), fImage,
                                                                                     sitoweb.get(), email.get()))
            else:
                c.execute(
                    "INSERT INTO prof VALUES ('{}','{}','{}','{}','{}','{}')".format(len(prof.keys()) + 1, nome.get(),
                                                                                     cognome.get(), "", sitoweb.get(),
                                                                                     email.get()))
            wa.destroy()
        elif mode == "edit":
            if "fImage" in globals() and not (fImage == None):
                c.execute("""UPDATE prof
                          SET nome = '{}', cognome = '{}', imageURI='{}', web='{}', email='{}'
                          WHERE ID={}; """.format(nome.get(), cognome.get(), fImage, sitoweb.get(), email.get(), idx))
            else:
                c.execute("""UPDATE prof
                          SET nome = '{}', cognome = '{}', imageURI='', web='{}', email='{}'
                          WHERE ID={}; """.format(nome.get(), cognome.get(), sitoweb.get(), email.get(), idx))
            we.destroy()
        elif mode == "del":
            c.execute("""DELETE FROM prof WHERE ID={};""".format(idx))
        sistemaIndici(conn, c)
        tkmb.showinfo(title=_("Successo!"), message=_("Salvataggio effettuato con successo!"))
        wip.destroy()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("Errore!"),
                       message=_(
                           "Si è verificato un errore, riprovare oppure contattare lo sviluppatore. Errore riscontrato:") + "\n" * 2 + str(
                           ex))


## MASCHERA DI ELIMINAZIONE ##
def delete():
    global selProf
    selProf = tp.item(tp.focus())
    if selProf["text"] == "":
        tkmb.showwarning(title=_("Nessun professore selezionato!"),
                         message=_(
                             "Non è stato selezionato nessun professore. Si prega di selezionarne uno per eliminarlo."))
        return ""
    scelta = tkmb.askyesno(title=_("Conferma eliminazione"),
                           message=_("Si è sicuri di voler eliminare il professore {} ?".format(
                               selProf["values"][1] + " " + selProf["values"][2])))
    if (scelta == True):
        Salvataggio("del", idx=selProf["text"])
    else:
        return ""


## SELEZIONE IMMAGINE ##
def selImmagine(bi, window):
    if not ("fImage" in globals()):
        global fImage
    fImage = askopenfilename(
        filetypes=[(_("File Immagini"), "*.jpg *.jpeg *.png *.bmp *.gif *.psd *.tif *.tiff *.xbm *.xpm *.pgm *.ppm")])
    if not (fImage == ""):
        bi["text"] = ""
    else:
        bi["text"] = _("Seleziona immagine")
    img = PIL.Image.open(fImage)
    # Ridimensionamento immagine a 100 px per larghezza, altezza variabile e scalata in base a quella vecchia e alla larghezza di 100 px
    basewidth = 100
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    photo = PIL.ImageTk.PhotoImage(img)
    bi["image"] = photo
    bi.image = photo
    if window == "wa":
        wa.geometry("350x{}+600+200".format(300 + hsize))
    elif window == "we":
        we.geometry("350x{}+600+200".format(300 + hsize))


## MASCHERA DI AGGIUNTA ##
def add():
    global wa
    wa = Toplevel()
    wa.configure(background="white")
    wa.title(_("Inserisci professore") + " - School Life Diary")
    wa.iconbitmap(r"images/sld_icon_beta.ico")
    wa.geometry("350x300+600+200")
    fap = Labelframe(wa, text=_("Maschera di inserimento"))
    fap.pack(padx=10, pady=10)
    ln = Label(fap, text=_("Nome:"))
    ln.grid(row=0, column=0, padx=10, pady=10)
    varn = StringVar(value="")
    en = Entry(fap, textvariable=varn)
    en.grid(row=0, column=1, padx=10, pady=10)
    varc = StringVar(value="")
    lc = Label(fap, text=_("Cognome:"))
    lc.grid(row=1, column=0, padx=10, pady=10)
    ec = Entry(fap, textvariable=varc)
    ec.grid(row=1, column=1, padx=10, pady=10)
    li = Label(fap, text=_("Immagine:"))
    li.grid(row=2, column=0, padx=10, pady=10)
    bi = Button(fap, text=_("Seleziona immagine"), command=lambda: selImmagine(bi, "wa"))
    bi.grid(row=2, column=1, padx=10, pady=10)
    varw = StringVar(value="")
    lw = Label(fap, text=_("Sito web:"))
    lw.grid(row=3, column=0, padx=10, pady=10)
    ew = Entry(fap, textvariable=varw)
    ew.grid(row=3, column=1, padx=10, pady=10)
    vare = StringVar(value="")
    le = Label(fap, text=_("Email:"))
    le.grid(row=4, column=0, padx=10, pady=10)
    ee = Entry(fap, textvariable=vare)
    ee.grid(row=4, column=1, padx=10, pady=10)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(wa, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio("add", varn, varc, varw, vare, None))
    b.pack(padx=10, pady=10)
    global fImage
    fImage = ""
    wa.mainloop()


## MASCHERA DI MODIFICA ##
def edit():
    global selProf
    selProf = tp.item(tp.focus())
    if selProf["text"] == "":
        tkmb.showwarning(title=_("Nessun professore selezionato!"),
                         message=_(
                             "Non è stato selezionato nessun professore. Si prega di selezionarne uno per apportare modifiche."))
        return ""
    global we
    we = Toplevel()
    we.configure(background="white")
    we.title(_("Modifica professore") + " - School Life Diary")
    we.iconbitmap(r"images/sld_icon_beta.ico")
    we.geometry("350x350+600+200")
    fap = Labelframe(we, text=_("Maschera di modifica"))
    fap.pack(padx=10, pady=10)
    ln = Label(fap, text=_("Nome:"))
    ln.grid(row=0, column=0, padx=10, pady=10)
    varn = StringVar(value=selProf["values"][0])
    en = Entry(fap, textvariable=varn)
    en.grid(row=0, column=1, padx=10, pady=10)
    varc = StringVar(value=selProf["values"][1])
    lc = Label(fap, text=_("Cognome:"))
    lc.grid(row=1, column=0, padx=10, pady=10)
    ec = Entry(fap, textvariable=varc)
    ec.grid(row=1, column=1, padx=10, pady=10)
    li = Label(fap, text=_("Immagine:"))
    li.grid(row=2, column=0, padx=10, pady=10)
    bi = Button(fap, text=_("Seleziona immagine"), command=lambda: selImmagine(bi, "we"))
    for i in prof:
        if prof[i]["nome"] == selProf["values"][0] and prof[i]["cognome"] == selProf["values"][1] and prof[i]["web"] == \
                selProf["values"][2] and prof[i]["email"] == selProf["values"][3] and not (selProf["image"] == ""):
            try:
                iprof = PIL.Image.open(prof[i]["imageURI"])
                # Ridimensionamento immagine a 100 px per larghezza, altezza variabile e scalata in base a quella vecchia e alla larghezza di 100 px
                basewidth = 100
                wpercent = (basewidth / float(iprof.size[0]))
                hsize = int((float(iprof.size[1]) * float(wpercent)))
                iprof = iprof.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
                pprof = PIL.ImageTk.PhotoImage(iprof)
                bi["image"] = pprof
                we.geometry("350x{}+600+200".format(300 + hsize))
            except FileNotFoundError:
                continue
    bi.grid(row=2, column=1, padx=10, pady=10)
    varw = StringVar(value=selProf["values"][2])
    lw = Label(fap, text=_("Sito web:"))
    lw.grid(row=3, column=0, padx=10, pady=10)
    fwww = Frame(fap)
    fwww.grid(row=3, column=1, padx=10, pady=10)
    ew = Entry(fwww, textvariable=varw)
    ew.grid(row=0, column=0, padx=10, pady=10)
    iwww = PIL.Image.open(r"icons/www.png")
    pwww = PIL.ImageTk.PhotoImage(iwww)
    bw = Button(fwww, image=pwww, compound=LEFT, width=0.5,
                command=lambda: webbrowser.open(varw.get()))
    bw.grid(row=0, column=1, padx=10)
    vare = StringVar(value=selProf["values"][3])
    le = Label(fap, text=_("Email:"))
    le.grid(row=4, column=0, padx=10)
    fmail = Frame(fap)
    fmail.grid(row=4, column=1, padx=10)
    em = Entry(fmail, textvariable=vare)
    em.grid(row=0, column=0, padx=10)
    imail = PIL.Image.open(r"icons/mail.png")
    pmail = PIL.ImageTk.PhotoImage(imail)
    bm = Button(fmail, image=pmail, compound=LEFT, width=1,
                command=lambda: webbrowser.open("mailto:{}".format(vare.get())))
    bm.grid(row=0, column=1, padx=10, pady=10)
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    b = Button(we, text=_("SALVA"), image=isave, compound=LEFT,
               command=lambda: Salvataggio("edit", varn, varc, varw, vare, selProf["text"]))
    b.pack(padx=10, pady=10)
    global fImage
    fImage = ""
    we.mainloop()


# MENU TASTO DESTRO
def popup(event):
    if event.widget != tp:
        return
    # display the popup menu
    try:
        aMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        aMenu.grab_release()


def popup2(event):
    if event.widget != wip:
        return
    # display the popup menu
    try:
        bMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        bMenu.grab_release()


# CREA FINESTRA
def creaFinestra():
    global wip
    wip = Toplevel()
    wip.configure(background="white")
    inizializza()
    wip.title(_("Professori") + " - School Life Diary")
    wip.iconbitmap(r"images/sld_icon_beta.ico")
    wip.geometry("1000x375+600+200")
    s = Style()
    sconn = sql.connect(os.path.join(path, "settings.db"), isolation_level=None)
    sc = sconn.cursor()
    s.theme_use(sc.execute("SELECT value FROM settings WHERE setting='PC_THEME'").fetchone())
    sc.close()
    s.configure("TFrame", background="white")
    s.configure("TLabelframe", background="white")
    s.configure("TLabelframe.Label", background="white")
    s.configure("TLabel", background="white")
    iAdd = PhotoImage(file=r"icons/add.png")
    iEdit = PhotoImage(file=r"icons/edit.png")
    iDel = PhotoImage(file=r"icons/delete.png")
    global aMenu
    aMenu = Menu(wip, tearoff=0)
    aMenu.add_command(label=_('Aggiungi'), image=iAdd, compound="left",
                      command=add)
    aMenu.add_command(label=_('Modifica'), image=iEdit, compound="left",
                      command=edit)
    aMenu.add_command(label=_('Elimina'), image=iDel, compound="left",
                      command=delete)
    global bMenu
    bMenu = Menu(wip, tearoff=0)
    bMenu.add_command(label=_('Aggiungi'), image=iAdd, compound="left",
                      command=add)
    global tp
    tp = Treeview(wip)
    tp.pack(padx=10, pady=10)
    tp["columns"] = ("nome", "cognome", "web", "email")
    tp.heading("#0", text=_("ID"))
    tp.column("#0", width=50)
    tp.heading("nome", text=_("Nome"))
    tp.column("nome", anchor=CENTER)
    tp.heading("cognome", text=_("Cognome"))
    tp.column("cognome", anchor=CENTER)
    tp.heading("web", text=_("Sito web"))
    tp.column("web", anchor=CENTER)
    tp.heading("email", text=_("Email"))
    tp.column("email", anchor=CENTER)
    tp.pack(padx=10, pady=10)
    tp.bind("<Double-Button-1>", lambda e: edit())
    tp.bind("<Button-3>", popup)
    iprof = PIL.Image.open(r"icons\picture.png")
    pprof = PIL.ImageTk.PhotoImage(iprof)
    for x in list(prof.keys()):
        if prof[x]["imageURI"] == "":
            tp.insert("", x, text=x, values=[prof[x]["nome"],
                                             prof[x]["cognome"],
                                             prof[x]["web"],
                                             prof[x]["email"]])
        else:
            if os.path.exists(prof[x]["imageURI"]):
                tp.insert("", x, text=x, values=[prof[x]["nome"],
                                                 prof[x]["cognome"],
                                                 prof[x]["web"],
                                                 prof[x]["email"]],
                          image=pprof)
            else:
                tp.insert("", x, text=x, values=[prof[x]["nome"],
                                                 prof[x]["cognome"],
                                                 prof[x]["web"],
                                                 prof[x]["email"]])
                tkmb.showwarning(_("Immagine non esistente!"),
                                 message=_(
                                     "Non esiste una immagine per il professore {}! Molto probabilmente l'hai spostata o eliminata. Per risolvere selezionare nuovamente l'immagine modificando il professore oppure spostarla nella cartella precedente.".format(
                                         prof[x]["nome"] + " " + prof[x]["cognome"])))
    li = Label(wip, text=_(
        "Per aggiungere un professore, usa il tasto destro del mouse su uno spazio vuoto della finestra.\nPer modificare un professore, fai doppio click sulla riga corrispondente.\nPer modificare o eliminare un professore, selezionare una riga e poi premere il tasto destro del mouse"))
    li.pack()
    wip.bind("<Button-3>", popup2)
    wip.focus()
    wip.mainloop()