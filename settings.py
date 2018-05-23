### SETTINGS.PY ###


## IMPORTAZIONE LIBRERIE E IMPOSTAZIONE CLIENT TRADUZIONI ##
from transifex.api import TransifexAPI

global tr
tr = TransifexAPI('sld', 'sld2017', 'https://www.transifex.com/')
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, Toplevel
import tkinter.messagebox as tkmb
import os.path  # serve per verificare se un file è presente o no
from zipfile import *
import subprocess
import time
import gettext
import ctypes
import locale
import polib
import PIL.Image
import PIL.ImageTk
import sqlite3 as sql
import wckToolTips
import style
from tkFontChooser import askfont
import datepicker

global path
global fn_set

## VARIABILI D'AMBIENTE ##
fn_set = "settings.db"
path = os.path.expanduser(r'~\Documents\School Life Diary')

## CREAZIONE DATABASE (PRIMO AVVIO) ##

output_filename = "settings.db"

if not (os.path.exists(path)):
    os.mkdir(path)
if not (os.path.exists(os.path.join(path, fn_set))):
    if os.path.exists(os.path.join(path, "settings.npy")):
        w.deiconify()
        tkmb.showwarning(title=_("Attenzione! Database non presente!"),
                         message=_(
                             "Non hai effettuato la migrazione del database. Il programma si avvierà, ma non saranno "
                             "visualizzati i tuoi dati fino a che non effettuerai la migrazione."))
        rd = tkmb.askokcancel(title=_("Conferma download strumento migrazione database"),
                              message=_("Vuoi scaricare lo strumento di migrazione del database?"))
        w.iconify()
        if rd is True:
            webbrowser.open("https://github.com/maicol07/school_life_diary_pc/releases")
    fs = open(os.path.join(path, fn_set), "w")
    fs.close()
    conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
    c = conn.cursor()
    c.execute("""CREATE TABLE `settings` ( `setting` TEXT,
                                                   `value` TEXT,
                                                   `descr` TEXT);""")
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("ORE_MAX_GIORNATA","5", "{}"); """.format(
        _("Numero di ore massime per giornate da visualizzare nell'orario")))
    if "win" == platform[:3]:
        th = 'vista'
    elif "darwin" in platform:
        th = 'clam'
    else:
        th = 'clam'
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("PC_THEME","{}", "{}"); """.format(th, _(
        "Tema visivo dell'applicazione")))
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("ALPHA_VERS", "{}", "{}");""".format(_("Sì"), _(
        "Consenso a ricevere notifiche di versioni alpha")))
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("BETA_VERS", "{}", "{}");""".format(_("No"), _(
        "Consenso a ricevere notifiche di versioni beta")))
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("PC_FONT", "{}", "{}");""".format("Helvetica", _(
        "Carattere utilizzato in tutti i testi dell'applicazione")))
    c.execute("""INSERT INTO settings (setting, value, descr) VALUES ("CHECK_UPDATES", "{}", "{}");""".format(_(
        "Sì"), _("Consenso a controllare all'avvio dell'app se sono disponibili aggiornamenti.")))
    c.execute("""INSERT INTO settings (setting, value, descr) VALUES ("PERIODS", "{}", "{}")""".format(
        "2 - 2018-09-15 - 2019-06-07", _("Periodi scolastici")))
else:
    conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings';")
    ris = c.fetchall()
    if not (len(ris) == 1):
        c.execute("""CREATE TABLE `settings` ( `setting` TEXT,
                                                   `value` TEXT,
                                                   `descr` TEXT);""")
    c.execute("SELECT * FROM settings")
    r = c.fetchall()
    if len(ris) == 0:
        c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("ORE_MAX_GIORNATA","5", "{}"); """.format(
            _("Numero di ore massime per giornate da visualizzare nell'orario")))
        if "win" == platform[:3]:
            th = 'vista'
        elif "darwin" in platform:
            th = 'clam'
        else:
            th = 'clam'
        c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("PC_THEME","{}", "{}"); """.format(th, _(
            "Tema visivo dell'applicazione")))
        c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("ALPHA_VERS", "{}", "{}");""".format(0, _(
            "Consenso a ricevere notifiche di versioni alpha")))
        c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("BETA_VERS", "{}", "{}");""".format(_("No"), _(
            "Consenso a ricevere notifiche di versioni beta")))
        c.execute(
            """INSERT INTO settings (setting,value,descr) VALUES ("PC_FONT", "{}", "{}");""".format("Helvetica", _(
                "Carattere utilizzato in tutti i testi dell'applicazione")))
        c.execute("""INSERT INTO settings (setting, value, descr) VALUES ("PERIODS", "{}", "{}")""".format(
            "2; 15/09/2018 - 23/12/2018; 09/01/2019 - 07/06/2019", _("Periodi scolastici")))

conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
c = conn.cursor()


def install_language():
    """
    Installa la lingua del modulo impostazioni.

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
        lg = gettext.translation("settings", localedir=os.path.join(path, 'locale'), languages=[lgcode[0:2]])
    else:
        fl = open(os.path.join(path, "language.txt"), "r")
        lgcode = fl.readline()
        lg = gettext.translation('settings', localedir=os.path.join(path, 'locale'), languages=[lgcode])
        fl.close()
    lg.install()


def salvaLingua(cb, mode):
    """
        MODALITA' 1: Salva la lingua scelta
        MODALITA' 2: Scarica le lingue aggiornate dal server di traduzione (Transifex)

        Parametri
        ----------
        :param cb : (Tkinter Combobox)
            Menu a tendina lingue.
        :param mode : (string)
            Modalità di avvio.

        Ritorna
        -------
        Niente
        """
    try:
        if mode == "download":
            l = sorted(["main", "settings", "note", "timetable", "subjects", "agenda", "voti"])
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
                          "La lingua scelta è stata salvata. L'applicazione ora si chiuderà, ricordati di RIAVVIARE "
                          "per RENDERE EFFETTIVE le modifiche!!"))
        exit()
    except Exception as ex:
        tkmb.showerror(title=_("Si è verificato un errore!!"),
                       message=_("È stato riscontrato un errore imprevisto. "
                                 "Riprovare o contattare lo sviluppatore.") + "\n" + str(ex))


def updatecb(cb, lang_list):
    """
        Aggiorna le opzioni del menu a tendina con le lingue nella lista.

        Parametri
        ----------
        :param cb : (string)
            Menu a tendina lingue.
        :param lang_list : (string)
            Lista delle lingue presenti.

        Ritorna
        -------
        Niente
        """
    cb["values"] = lang_list


def cambiaLingua():
    """
        Schermata cambio lingua

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    install_language()
    wl = Toplevel()
    wl.configure(background="white")
    wl.title(_("Cambia lingua") + " - School Life Diary")
    wl.iconbitmap(r"images/school_life_diary.ico")
    wl.geometry("500x250+100+100")
    languages_list = os.listdir(os.path.join(path, "locale"))
    e1 = Label(wl, text=_("Scegliere la propria lingua: "))
    cb = Combobox(wl, postcommand=lambda: updatecb(cb, languages_list))
    e1.pack(padx=10, pady=10)
    cb.pack(padx=10, pady=10)
    global ichange, idown
    pchange = PIL.Image.open(r"icons/restore.png")
    ichange = PIL.ImageTk.PhotoImage(pchange)
    pdown = PIL.Image.open(r"icons/download.png")
    idown = PIL.ImageTk.PhotoImage(pdown)
    btn = Button(wl, text=_("CAMBIA"), image=ichange, compound=LEFT, command=lambda: salvaLingua(cb, "change"))
    btn.pack(padx=10, pady=10)
    l = Label(wl, text=_("Scarica lingue non presenti nella lista\n o aggiorna quelle esistenti "
                         "dalla nostra piattaforma di traduzione."))
    l.pack(padx=10, pady=2)
    btn1 = Button(wl, text=_("SCARICA O AGGIORNA LINGUE"), image=idown, compound=LEFT,
                  command=lambda: salvaLingua(cb, "download"))
    btn1.pack(padx=5, pady=10)


def backup():
    """
        Backup dei dati dell'applicazione

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    fn_bk = "backups"
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
                  message="{0}{1}".format(_("""Backup creato con successo!
Puoi trovare il backup nella cartella appena aperta o al seguente percorso del tuo computer: """),
                                          os.path.join(path, fn_bk,
                                                       "backup-{}-{}.zip".format(time.strftime("%d-%m-%Y"),
                                                                                 time.strftime(
                                                                                     "%H-%M-%S")))))


def ripristino():
    """
        Ripristino dei dati da un file di backup.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
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
                           "Purtroppo il ripristino non è riuscito. Riprova, anche con un backup diverso, "
                           "oppure contattare lo sviluppatore.") + "\n" + ex)

    # ELIMINAZIONE DI TUTTI I DATI


def cancellatutto():
    """
        Cancella tutti i dati dell'applicazione.

        Parametri
        ----------
        Nessuno

        Ritorna
        -------
        Niente
        """
    tkmb.showinfo(title=_("Come cancellare i dati?"),
                  message=_("""Dalla versione 1.0 di School Life Diary, con il cambiamento del database da file a 
                  SQLite, non è più possibile cancellare i dati all'interno dell'app. È possibile, tuttavia, 
                  cancellare i file .db che trovi nella cartella dell'applicazione (in Documenti\School Life Diary). 
                  La cartella si aprirà dopo che hai premuto OK. 

Il software si chiuderà automaticamente dopo che la cartella si è aperta, per permettere la corretta eliminazione dei 
dati."""))
    subprocess.Popen(r'explorer "{}"'.format(path))
    exit()


def salvaImpostazioni(par, val):
    """
        Salva l'impostazione modificata.

        Parametri
        ----------
        :param par : (string)
            Nome del parametro modificato
        :param val : (string)
            Valore del parametro modificato.

        Ritorna
        -------
        Niente
        """
    try:
        sql_conn = sql.connect(os.path.join(path, fn_set), isolation_level=None)
        sql_cur = sql_conn.cursor()
        # if par == "ORE_MAX_GIORNATA":
        # c.execute("""UPDATE settings SET value = '{}' WHERE setting='{}';""".format(str(int(val)), par))
        # else:
        sql_cur.execute("""UPDATE settings SET value = '{}' WHERE setting='{}';""".format(val, par))
        tkmb.showinfo(title=_("Successo!"),
                      message=_("Parametro modificato con successo!"))
        if par == "PERIODS":
            wp.destroy()
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
            s.configure(".", font=sql_cur.execute("SELECT value FROM settings WHERE setting='PC_FONT'").fetchone()[0])
        if par == "PC_FONT":
            s = style.s
            s.configure(".", font=val)
        sql_cur.close()
        sql_conn.close()
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("ERRORE!"),
                       message=_("Si è verificato un errore durante la modifica del parametro. "
                                 "Riprovare o contattare lo sviluppatore! Errore riscontrato:\n") + str(ex))


# noinspection PyUnusedLocal
def accept_whole_number_only(sv, e=None):
    """
        Accetta solo valori interi nello slider

        Parametri
        ----------
        :param sv : (string)
            Slider valori.
        :param e : (event)
            Evento.

        Ritorna
        -------
        Niente
        """
    value = sv.get()
    if int(value) != value:
        sv.set(int(round(value)))


def inizializza(cursor):
    """
        Inizializzazione modulo annotazioni:
            • Crea dizionario con tutte le annotazioni, recuperate dal database

        Parametri
        ----------
        :param cursor : (sqlite3.Cursor)
            Cursore per la connessione al database.

        Ritorna
        -------
        Niente
        """
    install_language()
    global ds
    ds = {}
    cursor.execute("SELECT * FROM settings")
    sr = cursor.fetchall()
    for row in sr:
        if row[0] == "ALPHA_VERS" or row[0] == "BETA_VERS" or row[0] == "CHECK_UPDATES":
            if row[1] == "1":
                ds[row[0]] = (_("Sì"), row[2])
            else:
                ds[row[0]] = (_("No"), row[2])
        else:
            ds[row[0]] = (row[1], row[2])


def fontcallback(fs, var):
    """
        Font picker. Seleziona il carattere da utilizzare all'interno dell'applicazione.

        Parametri
        ----------
        :param fs : (Tkinter.Label)
            Etichetta font selezionato.
        :param var : (StringVar)
            Variabile che contiene il font selezionato.

        Ritorna
        -------
        Niente
        """
    # chiedi il font all'utente
    font = askfont(wcv, title=_("Selettore carattere"))
    # la variabile font è "" se l'utente ha annullato
    if font:
        # spaces in the family name need to be escaped
        font['family'] = font['family'].replace(' ', '\ ')
        font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
        if font['underline']:
            font_str += ' underline'
        if font['overstrike']:
            font_str += ' overstrike'
        fs.configure(font=font_str, text=_("Carattere selezionato: {}").format(font_str.replace('\ ', ' ')))
        var.set(font_str)


def modifica_valore(event):
    """
        Modifica l'impostazione.

        Parametri
        ----------
        :param event : (Treeview callback event)
            Evento che determina la pressione

        Ritorna
        -------
        • Niente
        """
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    try:
        par = item['values'][0]
    except IndexError:
        tkmb.showwarning(_("Nessun parametro selezionato!"),
                         _("Non hai selezionato nessun parametro!! Selezionane uno e poi ripeti l'operazione!"))
        return
    global wcv, bts
    wcv = Toplevel()
    wcv.configure(background="white")
    wcv.title(_("Cambia valore - Impostazioni") + " - School Life Diary")
    wcv.iconbitmap(r"images/school_life_diary.ico")
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
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT,
                     command=lambda: salvaImpostazioni(par, int(sv.get())))
    elif par == "PC_THEME":
        etichetta1 = Label(wcv, text=_("Scegliere il valore da attribuire al parametro:"))
        etichetta1.pack(padx=10, pady=10)
        menut = Combobox(wcv, postcommand=lambda: updateList(menut, style.s.theme_names()))
        menut.set(item["values"][1])
        menut.pack(padx=10, pady=10)
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT,
                     command=lambda: salvaImpostazioni(par, menut.get()))
    elif par == "ALPHA_VERS" or par == "BETA_VERS" or par == "CHECK_UPDATES":
        if par != "CHECK_UPDATES":
            etichetta1 = Label(wcv, text=_("Modifica il consenso per ricevere versioni non stabili:"))
        else:
            etichetta1 = Label(wcv, text=_("Modifica il consenso per controllare gli aggiornamenti all'avvio "
                                           "dell'applicazione."))
        etichetta1.pack(padx=10, pady=10)
        var = IntVar()
        if item["values"][1] == _("Sì"):
            var.set(1)
        else:
            var.set(0)
        if par == "ALPHA_VERS":
            etwar = Label(wcv, text=_("Le versioni Alpha sono poco stabili e non adatte all'uso\n"
                                      "quotidiano. Possono contenere parecchi problemi, ma vengono\n"
                                      "aggiornate più frequentemente rispetto alle versioni beta e stabili."))
            etwar.pack(padx=10, pady=10)
            cb = Checkbutton(wcv, text=_("Ricevi versioni alpha"), variable=var)
        elif par == "BETA_VERS":
            etwar = Label(wcv, text=_("Le versioni Beta sono abbastanza stabili e abbastanza adatte all'uso\n"
                                      "quotidiano. Possono contenere alcuni problemi, ma vengono\n"
                                      "aggiornate più frequentemente rispetto alle versioni stabili."))
            etwar.pack(padx=10, pady=10)
            cb = Checkbutton(wcv, text=_("Ricevi versioni beta"), variable=var)
        elif par == "CHECK_UPDATES":
            cb = Checkbutton(wcv, text=_("Controlla aggiornamenti all'avvio di School Life Diary"), variable=var)
        cb.pack(padx=10, pady=3)
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT,
                     command=lambda: salvaImpostazioni(par, var.get()))
    elif par == "PC_FONT":
        etichetta1 = Label(wcv, text=_('Scegli il carattere da utilizzare: '))
        etichetta1.pack(padx=10, pady=10)
        fc = Label(wcv, text=_("Carattere attuale: {}").format(item["values"][1]))
        fc.pack(padx=10, pady=10)
        font_selezionato = Label(wcv)
        font_selezionato.pack()
        var = StringVar(value=item["values"][1])
        btn = Button(wcv, text=_('Scegli carattere'), command=lambda: fontcallback(font_selezionato, var))
        btn.pack(padx=10, pady=10)
        bts = Button(wcv, text=_("SALVA"), image=isave, compound=LEFT,
                     command=lambda: salvaImpostazioni(par, var.get()))
    elif par == "PERIODS":
        def periods(per):
            def saveperiods():
                string = ""
                for x in var_list:
                    string += "{} - {}; ".format(globals()["d1_{}".format(x)].get(), globals()["d2_{}".format(x)].get())
                print(string)
                salvaImpostazioni(par, "{}; {}".format(per, string[:-2]))

            global wp
            wp = Toplevel()
            wp.configure(background="white")
            wp.geometry("525x{}+200+400".format(200 + 100 * per))
            wp.title(_("Cambia valore - Periodi - Impostazioni") + " - School Life Diary")
            wp.iconbitmap(r"images/school_life_diary.ico")
            e = Label(wp, text=_("Imposta le date di inizio/fine dei due periodi scolastici"))
            e.pack(pady=5)
            var_list = []
            periods_list = item["values"][1].split(";")
            for i in range(1, per + 1):
                fp = Labelframe(wp, text=_("Periodo n. {}").format(i))
                fp.pack(padx=5, pady=10)
                l1 = Label(fp, text=_("Data di inizio"))
                l2 = Label(fp, text=_("Data di fine"))
                l1.grid(row=0, column=0, padx=5)
                l2.grid(row=0, column=1)
                globals()["d1_{}".format(i)] = datepicker.Datepicker(fp)
                globals()["d1_{}".format(i)].grid(row=1, column=0, padx=5, pady=2)
                globals()["d2_{}".format(i)] = datepicker.Datepicker(fp)
                if i in range(len(periods_list)):
                    globals()["d1_{}".format(i)].date_var.set(periods_list[i].split(" - ")[0][1:])
                    globals()["d2_{}".format(i)].date_var.set(periods_list[i].split(" - ")[1])
                globals()["d2_{}".format(i)].grid(row=1, column=1, pady=2)
                var_list.append(i)
            btn_save = Button(wp, text=_("SALVA"), image=isave, compound=LEFT, command=lambda: saveperiods())
            btn_save.pack()
            wp.focus()
            wp.mainloop()

        etichetta1 = Label(wcv, text=_("Imposta il numero di periodi"))
        etichetta1.pack(pady=10)
        var = IntVar()
        var.set(item["values"][1].split(";")[0])
        num_per = Scale(wcv, variable=var, from_=1, to=6, orient=HORIZONTAL,
                        command=lambda e: accept_whole_number_only(num_per))
        num_per.pack()
        lvar = Label(wcv, textvariable=var)
        lvar.pack(padx=10, pady=2)
        bts = Button(wcv, text=_("OK"), command=lambda: periods(var.get()))

    bts.pack(padx=10, pady=10)
    wcv.focus()
    wcv.mainloop()


def updateList(menut, l):
    """
        Impostazione elementi menu a tendina

        Parametri
        ----------
        :param menut : (Tkinter Combobox)
            Menu a tendina vuoto
        :param l : (list)
            Lista con i valori da aggiungere al menu a tendina.

        Ritorna
        -------
        Niente
        """
    menut["values"] = sorted(l)


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
    if event.widget != ts:
        return
    i_edit = PhotoImage(file=r"icons/edit.png")
    s_menu = Menu(ws, tearoff=0)
    s_menu.add_command(label=_('Modifica'), image=i_edit, compound="left",
                       command=lambda: modifica_valore(event))
    # mostra il menu popup
    try:
        s_menu.tk_popup(event.x_root + 53, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        s_menu.grab_release()


# CREAZIONE FINESTRA
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
    connection = sql.connect(os.path.join(path, fn_set), isolation_level=None)
    cur = connection.cursor()
    inizializza(cur)
    global ws
    ws = Toplevel()
    ws.configure(bg="white")
    ws.title(_("Impostazioni") + " - School Life Diary")
    ws.iconbitmap(r"images/school_life_diary.ico")
    ws.geometry("1050x400+450+250")
    frame_imp = Labelframe(ws, text=_("Parametri"))
    frame_imp.pack()
    global ts
    ts = Treeview(frame_imp)
    ts["columns"] = ("par", "val_att", "descr")
    ts.heading("#0", text=_("ID"))
    ts.column("#0", width=30)
    ts.heading("par", text=_("Parametro"), anchor=CENTER)
    ts.column("par", anchor=CENTER)
    ts.heading("val_att", text=_("Valore attuale"))
    ts.column("val_att", width=325, anchor=CENTER)
    ts.heading("descr", text=_("Descrizione"))
    ts.column("descr", width=450, anchor=CENTER)
    ts.bind("<Double-Button-1>", modifica_valore)
    ts.bind("<Button-3>", popup)
    ts.pack()
    for x in range(len(list(ds))):
        e = ds[list(ds.keys())[x]]
        ts.insert("", "end", text=x + 1, values=[list(ds.keys())[x], e[0], _(e[1])])
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
    cur.close()
    connection.close()
    ws.mainloop()


c.close()
conn.close()
