import ctypes
import gettext
import locale
import os.path
import shutil
import sqlite3 as sql
import sys
import time
import tkinter.messagebox as tkmb

import polib
from babel import Locale
from transifex.api import TransifexAPI

from common import variables

### IMPOSTAZIONE PERCORSO DEI MODULI ###
sys.path.insert(0, '../modules')

variables.path_init()
path = variables.path


class Language(object):
    languages = []

    def __init__(self, domain):
        if not (os.path.exists(os.path.join(path, "locale"))):
            self.download_languages()
        if not (os.path.exists(os.path.join(path, "language.txt"))):
            lgcode = self.auto_recognize_language()
            lg = gettext.translation(domain, localedir=os.path.join(path, 'locale'), languages=[lgcode])
        else:
            try:
                fl = open(os.path.join(path, "language.txt"), "r")
                lgcode = fl.readline()
                if lgcode == "":
                    lgcode = self.auto_recognize_language()
                    lg = gettext.translation(domain, localedir=os.path.join(path, 'locale'), languages=[lgcode])
                else:
                    lg = gettext.translation(domain, localedir=os.path.join(path, 'locale'), languages=[lgcode])
            except FileNotFoundError:
                lgcode = self.auto_recognize_language()
                lg = gettext.translation(domain, localedir=os.path.join(path, 'locale'), languages=[lgcode])
            except Exception as ex:
                try:
                    tkmb.showerror(title=_("Lingua non impostata!"),
                                   message=_(
                                       r"La lingua impostata non è stata riconosciuta. Per risolvere prova a eliminare "
                                       r"il file in Documenti/School Life Diary/language.txt . Se il problema non si "
                                       r"risolve, contattare lo sviluppatore. Errore: ") + str(ex))
                except NameError:
                    tkmb.showerror(title="Can't install the language!",
                                   message=r"Can't recognize the set language. To fix this try to delete the file in "
                                           r"Documents/School Life Diary/language.txt . If the problem still occurs, "
                                           r"contact the developer. Error: " + str(ex))
        lg.install()
        try:
            locale.setlocale(locale.LC_ALL, lgcode)
        except locale.Error:
            import _locale
            _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
        self.lgcode = lgcode

    def auto_recognize_language(self):
        windll = ctypes.windll.kernel32
        lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        return lgcode

    def download_languages(self, cb=None):
        try:
            tr = TransifexAPI('sld', 'sld2017', 'https://www.transifex.com/')
            resources = tr.list_resources("school-life-diary-pc")
            resources_slugs = []
            for i in resources:
                resources_slugs.append(i["slug"])
            for i in resources_slugs:
                lang = tr.list_languages('school-life-diary-pc', i)
                i = i.replace("pot", "")
                for y in lang:
                    pathdl = os.path.join(path, 'locale', y, "LC_MESSAGES")
                    if not (os.path.exists(os.path.join(pathdl, (i + '.po')))):
                        if not (os.path.exists(os.path.join(pathdl))):
                            os.makedirs(os.path.join(pathdl))
                    tr.get_translation('school-life-diary-pc', i + "pot", y, os.path.join(pathdl, (i + '.po')))
                    po = polib.pofile(os.path.join(pathdl, (i + '.po')))
                    po.save_as_mofile(os.path.join(pathdl, (i + '.mo')))
            fdata = open(os.path.join(path, r"last_update_lang.txt"), "w")
            day = time.strftime("%c")
            fdata.write(day)
            fdata.close()
            if cb is not None:
                tkmb.showinfo(title=_("Lingue scaricate/aggiornate"),
                              message=_("Le lingue sono state scaricate. Puoi selezionarne una dal menu."))
                self.updatecb(cb)
        except ConnectionError as ex:
            if os.path.exists("locale"):
                shutil.copy("locale", path)
            else:
                tkmb.showerror(title="Can't download languages!",
                               message="There is no internet connection, so School Life Diary can't download "
                                       "translations. Reopen the app and retry with an internet connection available."
                                       "\nError: " + str(ex))

    def get_language_name(self, lgcode=None):
        if lgcode is None:
            lgcode = self.auto_recognize_language()
        lcode = lgcode.split("_")
        langname = Locale(lcode[0], lcode[1]).display_name
        return langname

    def updatecb(self, cb):
        """
            Aggiorna le opzioni del menu a tendina con le lingue nella lista.

            Parametri
            ----------
            :param cb : (string)
                Menu a tendina lingue.

            Ritorna
            -------
            Niente
            """
        global langd
        langd = {}
        lang_folder_list = os.listdir(os.path.join(path, "locale"))
        for code in lang_folder_list:
            langd[code] = lang.get_language_name(code)
        lang_list = list(langd.values())
        self.languages = langd
        cb["values"] = lang_list

    def saveLanguage(self, cb):
        """
            Salva la lingua scelta

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
            codes = list(self.languages.keys())
            lang_names = [x.lower() for x in list(self.languages.values())]
            newlang = codes[lang_names.index(cb.get().lower())]
            f = open(os.path.join(path, "language.txt"), "w")
            f.write(newlang)
            f.close()
            restart = tkmb.showinfo(title=_("Salvataggio effettuato"),
                                    message=_("La lingua scelta è stata salvata. Vuoi riavviare School Life Diary per "
                                              "applicare le modifiche?"))
            if restart is True:
                os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as ex:
            tkmb.showerror(title=_("Si è verificato un errore!"),
                           message=_("È stato riscontrato un errore imprevisto. "
                                     "Riprovare o contattare lo sviluppatore.") + "\n" + str(ex))


class Update(object):
    def __init__(self):
        self.check_updates()

    def check_updates(self):
        ### Verifica se esistono degli aggiornamenti per il programma ###
        global v
        vs = "alpha"
        v = variables.version
        if not (os.path.exists(os.path.join(path, "version.txt"))):
            fv = open(os.path.join(path, "version.txt"), "w")
            fv.write(v)
            fv.close()
        else:
            fv = open(os.path.join(path, "version.txt"), "r")
            pv = fv.readline()
            if pv < v:
                if vs == "alpha":
                    tkmb.showwarning(_("Versione non stabile rilevata!"),
                                     message=_(
                                         "La versione che stai utilizzando è una versione ALPHA non stabile, che può "
                                         "contenere bug e problemi vari, anche gravi. Ti consigliamo di non usare "
                                         "questa versione in ambito produttivo."))
                elif vs == "beta":
                    tkmb.showwarning(_("Versione BETA non stabile rilevata!"),
                                     message=_(
                                         "La versione che stai utilizzando è una versione BETA non stabile, che può "
                                         "contenere piccoli bug e problemi. Puoi usare questa versione in ambito "
                                         "produttivo, ma segnala i bug, se dovessi incontrarne uno, in vista del "
                                         "rilascio stabile."))
                self.upgrade(pv, v)
                fv.close()
                fv = open(os.path.join(path, "version.txt"), "w")
                fv.write(v)
            fv.close()
        if db.c.execute("SELECT value FROM settings WHERE setting='CHECK_UPDATES'", fetch="one").fetchone() == _("Sì"):
            feed_name = "School Life Diary Releases"
            url = r"https://github.com/maicol07/school_life_diary_pc/releases.atom"
            feed = feedparser.parse(url)
            try:
                post = feed.entries[0]
                title = post.title
                lp = title.split(" ")
                ac = db.c.execute("SELECT value FROM settings WHERE setting='ALPHA_VERS'").fetchone()
                bc = db.c.execute("SELECT value FROM settings WHERE setting='BETA_VERS'").fetchone()
                if lp[0][1:].isdecimal() is True:
                    lp[0] = lp[0][1:]
                if v != lp[0][1:]:
                    w.deiconify()
                    if lp[0][0].lower() == "v":
                        agg = tkmb.askyesno(title=_("Nuova versione disponibile!"),
                                            message=_("È disponibile una nuova versione stabile di School Life Diary. "
                                                      "Ti consigliamo di aggiornare il prima possibile per non perdere "
                                                      "le nuove funzionalità, i miglioramenti e le correzioni di "
                                                      "problemi. Vuoi accedere alla pagina da cui scaricare l'"
                                                      "aggiornamento alla versione stabile {}?").format(lp[0][1:]))
                    elif lp[0][0].lower() == "b" and bc == _("Sì"):
                        agg = tkmb.askyesno(title=_("Nuova versione BETA disponibile!"),
                                            message=_("È disponibile una nuova versione BETA di School Life Diary. "
                                                      "Queste versioni non sono del tutto stabili e possono contenere "
                                                      "alcuni problemi, ma includono nuove funzionalità. Ricevi questo "
                                                      "avviso perchè hai dato il tuo consenso a ricevere le notifiche "
                                                      "di versioni BETA Vuoi accedere alla pagina da cui scaricare l'"
                                                      "aggiornamento alla versione BETA {}?").format(lp[0][1:]))
                    elif lp[0][0].lower() == "a" and ac == _("Sì"):
                        agg = tkmb.askyesno(title=_("Nuova versione ALPHA disponibile!"),
                                            message=_("È disponibile una nuova versione ALPHA di School Life Diary. "
                                                      "Queste versioni non sono stabili e possono contenere parecchi "
                                                      "problemi, ma includono nuove funzionalità. Ricevi questo avviso "
                                                      "perchè hai dato il tuo consenso a ricevere le notifiche di nuove"
                                                      " versioni ALPHA. Vuoi accedere alla pagina da cui scaricare l'"
                                                      "aggiornamento alla versione ALPHA {}?").format(lp[0][1:]))
                    if agg is True:
                        webbrowser.open("https://github.com/maicol07/school_life_diary_pc/releases/")
                    w.iconify()
            except IndexError:
                w.deiconify()
                tkmb.showwarning(title=_("Nessuna connessione ad internet"),
                                 message=_(
                                     "Non è disponibile nessuna connessione ad internet per la ricerca degli aggiornamenti. La "
                                     "ricerca verrà ritentata la prossima volta che sarà riaperto il programma."))
                w.iconify()

    def upgrade(self, prev_vers, target_version):
        """
        Esegue l'aggiornamento del database alla versione installata

        Parametri
        ----------
        :param prev_vers : (string)
            Parametro che identifica la versione precedente del software.
        :param target_version : (string)
            Parametro che identifica la nuova versione a cui si è aggiornato il software.

        Ritorna
        -------
        Niente

        Errori
        ------
        TimeOutError
            Quando è impossibile stabilire una connessione con l'host.
        """
        from bs4 import BeautifulSoup
        import requests
        import urllib.request

        update_url = 'https://www.school-life-diary.tk/appupdates/pc'
        extension = 'txt'

        def listFD(updateurl, ext=''):
            """
                Recupera gli aggiornamenti (le query SQL) dal server.

                Parametri
                ----------
                :param updateurl : (string)
                    Parametro che identifica l'url da cui scaricare gli aggiornamenti da eseguire.
                :param ext : (string)
                    Parametro che identifica l'estensione del file da scaricare.

                Ritorna
                -------
                Lista con tutti i file recuperati dall'URL
                """
            page = requests.get(updateurl).text
            soup = BeautifulSoup(page, 'html.parser')
            return [updateurl + '/' + node.get('href') for node in soup.find_all('a') if
                    node.get('href').endswith(ext)]

        while prev_vers != target_version:
            for file in listFD(update_url, extension):
                lf = file.split("/")
                lv = lf[-1].split("-")
                if lv[0] == prev_vers:
                    try:
                        data = urllib.request.urlopen(file)
                    except TimeoutError:
                        tkmb.showerror(_("Impossibile stabilire la connessione"),
                                       message=_("[WinError 10060] Impossibile stabilire la connessione."
                                                 "Risposta non corretta della parte connessa dopo l'intervallo "
                                                 "di tempo oppure mancata risposta dall'host collegato. Riaprire l'app e"
                                                 " riprovare."))
                        exit()
                    for i in data:
                        if not (" " in str(i)):
                            try:
                                cur.close()
                                connection.close()
                            except:
                                pass
                            connection = sql.connect(os.path.join(path, str(i)[2:-3]))
                            cur = connection.cursor()
                        else:
                            cur.execute(str(i)[2:-3])
                    try:
                        cur.close()
                        connection.close()
                    except:
                        pass
                    prev_vers = lv[1][:-4]


class FirstRun(object):
    def __init__(self):
        if not (os.path.exists(os.path.join(path, "data.db"))):
            self.create_db()
            Language().download_languages()

    def create_db(self):
        if os.path.exists(os.path.join(path, "settings.npy")):
            w.deiconify()
            tkmb.showwarning(title=_("Attenzione! Database non presente!"),
                             message=_(
                                 "Non hai effettuato la migrazione del database. Il programma si avvierà, ma non "
                                 "saranno visualizzati i tuoi dati fino a che non effettuerai la migrazione."))
            rd = tkmb.askokcancel(title=_("Conferma download strumento migrazione database"),
                                  message=_("Vuoi scaricare lo strumento di migrazione del database?"))
            w.iconify()
            if rd is True:
                webbrowser.open("https://github.com/maicol07/school_life_diary_pc/releases")
        if os.path.exists(os.path.join(path, "settings.db")):
            fs = open(os.path.join(path, "data.db"), "w")
            fs.close()
            l = sorted(["main", "settings", "note", "timetable", "subjects", "agenda", "voti"])
            for i in l:
                conn, c = connect_database(i)
                with open(os.path.join(path, 'dump.sql'), 'w') as f:
                    for line in conn.iterdump():
                        f.write('{}\n'.format(line))
                    f.close()
                close_database(conn, c)
                shutil.copy(os.path.join(path, i + ".db"), os.path.join(path, i + ".db.bak"))
                shutil.copy(os.path.join(path, "data.db"), os.path.join(path, "data.db.bak"))
                f = open(os.path.join(path, 'dump.sql'), 'r')
                sql = f.read().replace('DELETE FROM "sqlite_sequence";', "")
                f.close()
                conn, c = connect_database()
                conn.executescript(sql)
                close_database(conn, c)
                os.remove(os.path.join(path, 'dump.sql'))
        conn, c = connect_database()
        if "win" == sys.platform[:3]:
            th = 'vista'
        elif "darwin" in sys.platform:
            th = 'clam'
        else:
            th = 'clam'
        c.executemany("""
        CREATE TABLE `settings` (`setting` TEXT,
        `value` TEXT,
        `descr` TEXT);
        
        INSERT INTO settings (setting,value,descr) VALUES ("ORE_MAX_GIORNATA","5", "?");
        
        INSERT INTO settings (setting,value,descr) VALUES ("PC_THEME","?", "?");
        
        INSERT INTO settings (setting,value,descr) VALUES ("ALPHA_VERS", "?", "?");
        
        INSERT INTO settings (setting,value,descr) VALUES ("BETA_VERS", "?", "?");
        
        INSERT INTO settings (setting,value,descr) VALUES ("PC_FONT", "?", "?");
        
        INSERT INTO settings (setting, value, descr) VALUES ("CHECK_UPDATES", "?", "?");
        
        INSERT INTO settings (setting, value, descr) VALUES ("PERIODS", "{}", "{}");""", [(
            _("Numero di ore massime per giornate da visualizzare nell'orario"),
            th,
            _("Tema visivo dell'applicazione"),
            _("No"),
            _("Consenso a ricevere notifiche di versioni alpha"),
            _("No"),
            _("Consenso a ricevere notifiche di versioni beta"),
            "TkDefaultFont",
            _("Carattere utilizzato in tutti i testi dell'applicazione"),
            _("Sì"),
            _("Consenso a controllare all'avvio dell'app se sono disponibili aggiornamenti."),
            "2 - 2018-09-15 - 2019-06-07",
            _("Periodi scolastici")
        )])
        close_database(conn, c)


def connect_database(module_name="data"):
    if not (os.path.exists(os.path.join(path, "{}.db".format(module_name)))):
        fm = open(os.path.join(path, "{}.db".format(module_name)), "w")
        fm.close()
    conn = sql.connect(os.path.join(variables.path, "{}.db".format(module_name)), isolation_level=None)
    c = conn.cursor()
    return conn, c


def close_database(conn, c):
    c.close()
    conn.close()


lang = Language("init")
FirstRun()
