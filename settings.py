### SETTINGS.PY ###


## IMPORTAZIONE LIBRERIE E IMPOSTAZIONE CLIENT TRADUZIONI ##
from transifex.api import TransifexAPI

global tr
tr = TransifexAPI('sld', 'sld2017', 'https://www.transifex.com')
from tkinter import *
from ttkthemes.themed_style import *
from tkinter.ttk import *
from tkinter import filedialog, Tk, Toplevel
import tkinter.messagebox as tkmb
import os.path  # serve per verificare se un file è presente o no
from zipfile import *
import subprocess, time, gettext, ctypes, locale, polib, PIL.Image, PIL.ImageTk
import sqlite3 as sql
import wckToolTips
import style

global path
global fn_set

## VARIABILI D'AMBIENTE ##
fn_set = "settings.db"
path = os.path.expanduser(r'~\Documents\School Life Diary')
conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
c = conn.cursor()

## INSTALLAZIONE LINGUA ##
if not (os.path.exists(os.path.join(path, "language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl = ["en", "it"]
    lg = gettext.translation("settings", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
else:
    fl = open(os.path.join(path, "language.txt"), "r")
    lgcode = fl.readline()
    lg = gettext.translation('settings', localedir=os.path.join(path, 'locale'), languages=[lgcode])
    fl.close()
lg.install()


## SALVATAGGIO LINGUA ##
def salvaLingua(cb, lgl, wl, mode):
    try:
        if mode == "download":
            l = ["main", "settings", "note", "timetable", "subject"]
            for i in l:
                lang = tr.list_languages('school-life-diary-pc', i + "pot")
                for y in lang:
                    pathdl = os.path.join(path, 'locale', y[:2], "LC_MESSAGES")
                    if not (os.path.exists(os.path.join(pathdl, (i + '.po')))):
                        if not (os.path.exists(os.path.join(pathdl))):
                            os.makedirs(os.path.join(pathdl))
                        '''filecreation = open(os.path.join(pathdl, (i + '.po')), "w")
                        filecreation.close()'''
                    tr.get_translation('school-life-diary-pc', i + "pot", y, os.path.join(pathdl, (i + '.po')))
                    po = polib.pofile(os.path.join(pathdl, (i + '.po')))
                    po.save_as_mofile(os.path.join(pathdl, (i + '.mo')))
        else:
            f = open(os.path.join(path, "language.txt"), "w")
            f.write(cb.get())
            f.close()
        tkmb.showinfo(title=_("Salvataggio effettuato"),
                      message=_(
                          "La lingua scelta è stata salvata. L'applicazione ora si chiuderà, ricordati di RIAVVIARE per RENDERE EFFETTIVE le modifiche!!"))
        exit()
    except Exception as ex:
        if str(ex) == "404: b'Not Found'":
            updatecb(cb, lgl)
            tkmb.showinfo(title=_("Lingue scaricate"),
                          message=_("La lingue sono state scaricate. Puoi sceglierne una dal menu!"))
            wl.destroy()
            cambiaLingua()
        else:
            tkmb.showerror(title=_("Si è verificato un errore!!"),
                           message=_(
                               "È stato riscontrato un errore imprevisto. Riprovare o contattare lo sviluppatore.") + "\n" + str(
                               ex))


## AGGIORNAMENTO LISTA LINGUE ##
def updatecb(cb, lgl):
    cb["values"] = lgl


## CAMBIO LINGUA ##
def cambiaLingua():
    wl = Toplevel()
    wl.configure(background="white")
    wl.title(_("Cambia lingua") + " - School Life Diary")
    wl.iconbitmap(r"images/sld_icon_beta.ico")
    wl.geometry("500x250+100+100")
    lgl = os.listdir(os.path.join(path, "locale"))
    e1 = Label(wl, text=_("Scegliere la propria lingua: "))
    cb = Combobox(wl, postcommand=lambda: updatecb(cb, lgl))
    e1.pack(padx=10, pady=10)
    cb.pack(padx=10, pady=10)
    global ichange, idown
    pchange = PIL.Image.open(r"icons/restore.png")
    ichange = PIL.ImageTk.PhotoImage(pchange)
    pdown = PIL.Image.open(r"icons/download.png")
    idown = PIL.ImageTk.PhotoImage(pdown)
    btn = Button(wl, text=_("CAMBIA"), image=ichange, compound=LEFT, command=lambda: salvaLingua(cb, lgl, wl, "change"))
    btn.pack(padx=10, pady=10)
    l = Label(wl, text=_(
        "Scarica lingue non presenti nella lista\n o aggiorna quelle esistenti dalla nostra piattaforma di traduzione."))
    l.pack(padx=10, pady=2)
    btn1 = Button(wl, text=_("SCARICA O AGGIORNA LINGUE"), image=idown, compound=LEFT,
                  command=lambda: salvaLingua(cb, lgl, wl, "download"))
    btn1.pack(padx=5, pady=10)


## BACKUP DEI DATABASE ##
def backup():
    fn_bk = "backups"
    bfoldpath = os.path.join(path, fn_bk)
    if not (os.path.exists(os.path.join(path, fn_bk))):
        os.mkdir(os.path.join(path, fn_bk))
    bzip = ZipFile(os.path.join(path,
                                fn_bk,
                                "backup-" + time.strftime("%d-%m-%Y") + "-" + time.strftime("%H-%M-%S") + ".zip"),
                   "w", ZIP_DEFLATED)
    filelist = [f for f in os.listdir(path) if f.endswith(".db")]
    for f in filelist:
        bzip.write(os.path.join(path, f), os.path.basename(os.path.join(path, f)))
    bzip.close()
    subprocess.Popen(r'explorer /select,"' + os.path.join(path,
                                                          fn_bk,
                                                          "backup-" + time.strftime("%d-%m-%Y") + "-" + time.strftime(
                                                              "%H-%M-%S") + ".zip") + '"')
    tkmb.showinfo(title=_("Backup effettuato!"),
                  message=_("""Backup creato con successo!
Puoi trovare il backup nella cartella appena aperta o al seguente percorso del tuo computer: """) + os.path.join(path,
                                                                                                                 fn_bk,
                                                                                                                 "backup-" + time.strftime(
                                                                                                                     "%d-%m-%Y") + "-" + time.strftime(
                                                                                                                     "%H-%M-%S") + ".zip"))


# RIPRISTINO DEI DATI DA BACKUP
def ripristino():
    try:
        bkpath = filedialog.askopenfilename()
        bk = ZipFile(bkpath, "r")
        bk.extractall(path)
        bk.close()
        tkmb.showinfo(title=_("Ripristino effettuato!"),
                      message=_("Backup ripristinato con successo! Riavvia per rendere effettive le modifiche!"))
    except FileNotFoundError:
        return
    except Exception as ex:
        tkmb.showerror(title=_("Ripristino non riuscito"),
                       message=_(
                           "Purtroppo il ripristino non è riuscito. Riprova, anche con un backup diverso, oppure contattare lo sviluppatore.") + "\n" + ex)


# ELIMINAZIONE DI TUTTI I DATI
def cancellatutto():
    tkmb.showinfo(title=_("Come cancellare i dati?"),
                  message=_("""Dalla versione 1.0 di School Life Diary, con il cambiamento del database da file a SQLite, non è più possibile cancellare i dati all'interno dell'app.
È possibile, tuttavia, cancellare i file .db che trovi nella cartella dell'applicazione (in Documenti\School Life Diary). La cartella si aprirà dopo che hai premuto OK.

Il software si chiuderà automaticamente dopo che la cartella si è aperta, per permettere la corretta eliminazione dei dati."""))
    subprocess.Popen(r'explorer "{}"'.format(path))
    exit()


# Salvataggio impostazioni
def salvaImpostazioni(par, val):
    try:
        conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
        c = conn.cursor()
        print(val)
        #if par == "ORE_MAX_GIORNATA":
        #c.execute("""UPDATE settings SET value = '{}' WHERE setting='{}';""".format(str(int(val)), par))
        #else:
        c.execute("""UPDATE settings SET value = '{}' WHERE setting='{}';""".format(val, par))
        tkmb.showinfo(title=_("Successo!"),
                      message=_(
                          "Parametro modificato con successo!\n\nRICORDATI DI RIAVVIARE L'APPLICAZIONE PER RENDERE EFFETTIVE LE MODIFICHE!!"))
        wcv.destroy()
        ws.destroy()
        if par == "PC_THEME":
            s = style.s
            s.set_theme(val)
            s.configure("TFrame", background="white")
            s.configure("TButton", height=100)
            s.configure("TLabel", background="white")
            s.configure("TPhotoimage", background="white")
            s.configure("TLabelframe", background="white")
            s.configure("TLabelframe.Label", background="white")
            s.configure("TScale", background="white")
            s.configure("TCheckbutton", background="white")
        c.close()
        conn.close()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("ERRORE!"),
                       message=_(
                           "Si è verificato un errore durante la modifica del parametro. Riprovare o contattare lo sviluppatore! Errore riscontrato:\n") + str(
                           ex))


# ACCETTAZIONE SOLO VALORI INTERI NELLO SLIDER
def accept_whole_number_only(sv, e=None):
    value = sv.get()
    if int(value) != value:
        sv.set(int(round(value)))


# INIZIALIZZAZIONE IMPOSTAZIONI
def inizializza(c):
    global ds
    ds = {}
    c.execute("SELECT * FROM settings")
    sr = c.fetchall()
    for row in sr:
        if row[0] == "ALPHA_VERS" or row[0] == "BETA_VERS":
            if row[1] == "1":
                print(1)
                ds[row[0]] = (_("Sì"), row[2])
            else:
                print(0)
                ds[row[0]] = (_("No"), row[2])
        else:
            ds[row[0]] = (row[1], row[2])


# MODIFICA VALORE DEL PARAMETRO
def modifica_valore(event):
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    try:
        par = item['values'][0]
    except IndexError:
        tkmb.showwarning(_("Nessun parametro selezionato!"),
                         _("Non hai selezionato nessun parametro!! Selezionane uno e poi ripeti l'operazione!"))
        return ""
    global wcv, bts
    wcv = Toplevel()
    wcv.configure(background="white")
    wcv.title(_("Cambia valore - Impostazioni") + " - School Life Diary")
    wcv.iconbitmap(r"images/sld_icon_beta.ico")
    wcv.geometry("400x200+600+250")
    psave = PIL.Image.open(r"icons/save.png")
    isave = PIL.ImageTk.PhotoImage(psave)
    if par == "ORE_MAX_GIORNATA":
        etichetta1 = Label(wcv, text=_("Scegliere il valore da attribuire al parametro:"))
        etichetta1.pack(padx=10, pady=10)
        var = IntVar()
        var.set(item["values"][1])
        sv = Scale(wcv, variable=var, from_=4, to=8, orient=HORIZONTAL, command=lambda e: accept_whole_number_only(sv))
        lvar = Label(wcv, textvariable=var)
        lvar.pack(padx=10, pady=2)
        sv.pack(padx=10, pady=10)
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: salvaImpostazioni(par, int(sv.get())))
    if par == "PC_THEME":
        etichetta1 = Label(wcv, text=_("Scegliere il valore da attribuire al parametro:"))
        etichetta1.pack(padx=10, pady=10)
        menut = Combobox(wcv, postcommand=lambda: updateList(menut, style.s.theme_names()))
        menut.set(item["values"][1])
        menut.pack(padx=10, pady=10)
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: salvaImpostazioni(par, menut.get()))
    if par == "ALPHA_VERS" or par == "BETA_VERS":
        etichetta1 = Label(wcv, text=_("Modifica il consenso per ricevere versioni non stabili:"))
        etichetta1.pack(padx=10, pady=10)
        var=IntVar()
        if item["values"][1] == _("Sì"):
            var.set(1)
        else:
            var.set(0)
        if par=="ALPHA_VERS":
            etwar = Label(wcv, text=_("Le versioni Alpha sono poco stabili e non adatte all'uso\n"
                                                "quotidiano. Possono contenere parecchi problemi, ma vengono\n"
                                                "aggiornate più frequentemente rispetto alle versioni beta e stabili."))
            c = Checkbutton(wcv, text=_("Ricevi versioni alpha"), variable=var)
        elif par == "BETA_VERS":
            etwar = Label(wcv, text=_("Le versioni Beta sono abbastanza stabili e abbastanza adatte all'uso\n"
                                                    "quotidiano. Possono contenere alcuni problemi, ma vengono\n"
                                                    "aggiornate più frequentemente rispetto alle versioni stabili."))
            c = Checkbutton(wcv, text=_("Ricevi versioni beta"), variable=var)
        etwar.pack(padx=10,pady=10)
        c.pack(padx=10,pady=3)
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: salvaImpostazioni(par, var.get()))
    bts.pack(padx=10, pady=10)
    wcv.focus()
    wcv.mainloop()


# IMPOSTAZIONE ELEMENTI MENU A TENDINA
def updateList(menut, l):
    menut["values"] = sorted(l)


# MENU TASTO DESTRO
def popup(event):
    if event.widget != ts:
        return
    iEdit = PhotoImage(file=r"icons/edit.png")
    sMenu = Menu(ws, tearoff=0)
    sMenu.add_command(label=_('Modifica'), image=iEdit, compound="left",
                      command=lambda: modifica_valore(event))
    # display the popup menu
    try:
        sMenu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        sMenu.grab_release()


# CREAZIONE FINESTRA
def creaFinestra():
    conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
    c = conn.cursor()
    inizializza(c)
    global ws
    ws = Toplevel()
    ws.configure(bg="white")
    ws.title(_("Impostazioni") + " - School Life Diary")
    ws.iconbitmap(r"images/sld_icon_beta.ico")
    ws.geometry("900x400+600+250")
    fs = Labelframe(ws, text=_("Parametri"))
    fs.pack()
    global ts
    ts = Treeview(fs)
    ts["columns"] = ("par", "val_att", "descr")
    ts.heading("#0", text=_("ID"))
    ts.column("#0", width=30)
    ts.heading("par", text=_("Parametro"), anchor=CENTER)
    ts.column("par", anchor=CENTER)
    ts.heading("val_att", text=_("Valore attuale"))
    ts.column("val_att", anchor=CENTER)
    ts.heading("descr", text=_("Descrizione"))
    ts.column("descr", width=450, anchor=CENTER)
    ts.bind("<Double-Button-1>", modifica_valore)
    ts.bind("<Button-3>", popup)
    ts.pack()
    for x in range(len(list(ds))):
        e = ds[list(ds.keys())[x]]
        ts.insert("", "end", text=x + 1, values=[list(ds.keys())[x], e[0], e[1]])
    li = Label(ws, text=_(
        "Per modificare un parametro, fai doppio click sulla riga corrispondente o tasto destro con il mouse."))
    li.pack()
    fbr = Labelframe(ws, text=_("Backup & Ripristino"))
    ibackup = PIL.Image.open(r"icons\download.png")
    pbackup = PIL.ImageTk.PhotoImage(ibackup)
    irestore = PIL.Image.open(r"icons\restore.png")
    prestore = PIL.ImageTk.PhotoImage(irestore)
    ideleteall = PIL.Image.open(r"icons\deleteall.png")
    pdeleteall = PIL.ImageTk.PhotoImage(ideleteall)
    ifolder = PIL.Image.open(r"icons\folder.png")
    pfolder = PIL.ImageTk.PhotoImage(ifolder)
    bb = Button(fbr, text=_("ESEGUI BACKUP"), image=pbackup, compound="left",
                command=backup)
    br = Button(fbr, text=_("ESEGUI RIPRISTINO"), image=prestore, compound=LEFT,
                command=ripristino)
    bc = Button(fbr, text=_("CANCELLA TUTTO"), image=pdeleteall, compound=LEFT,
                command=cancellatutto)
    bf = Button(fbr, text=_("APRI CARTELLA LOCALE"), image=pfolder, compound=LEFT,
                command=lambda: subprocess.Popen(r'explorer "{}"'.format(path)))
    fbr.pack()
    bb.grid(row=0, column=0, padx=10, pady=10)
    br.grid(row=0, column=1, padx=10, pady=10)
    bc.grid(row=0, column=2, padx=10, pady=10)
    bf.grid(row=0, column=3, padx=10, pady=10)
    wckToolTips.register(bf, _("Apri la cartella dei dati di School Life Diary (con tutti i file dei database)"))
    ws.focus()
    c.close()
    conn.close()
    ws.mainloop()

c.close()
conn.close()