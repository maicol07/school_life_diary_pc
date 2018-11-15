import ctypes
import gettext
import locale
import os.path
import sqlite3 as sql
import sys
import tkinter.messagebox as tkmb

### IMPOSTAZIONE PERCORSO LIBRERIE ESTERNE ###
sys.path.insert(0, '../modules')
from modules import variables

path = variables.path


class Language(object):
    def __init__(self, domain):
        if not (os.path.exists(os.path.join(path, "language.txt"))):
            windll = ctypes.windll.kernel32
            lgcode = locale.windows_locale[windll.GetUserDefaultUILanguage()]
            lg = gettext.translation(domain, localedir=os.path.join(path, 'locale'), languages=[lgcode])
        else:
            try:
                fl = open(os.path.join(path, "language.txt"), "r")
                lgcode = fl.readline()
                lg = gettext.translation(domain, localedir=os.path.join(path, 'locale'), languages=[lgcode])
            except Exception as ex:
                w.deiconify()
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
                                           r"contact the developer. Error: ") + str(
                        ex)
                w.withdraw()
        lg.install()
        locale.setlocale(locale.LC_ALL, lgcode)


def create_database(db_name):
    conn = sql.connect(os.path.join(variables.path, db_name + ".db"), isolation_level=None)
    c = conn.cursor()
    return conn, c


def close_database(conn, c):
    c.close()
    conn.close()


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
                                         "contenere bug e problemi vari, anche gravi. Ti consigliamo di non usare questa "
                                         "versione in ambito produttivo."))
                elif vs == "beta":
                    tkmb.showwarning(_("Versione BETA non stabile rilevata!"),
                                     message=_(
                                         "La versione che stai utilizzando è una versione ALPHA non stabile, che può"
                                         "contenere piccoli bug e problemi. Puoi usare questa versione in ambito"
                                         "produttivo, ma segnala i bug, se dovessi incontrarne uno, in vista del rilascio"
                                         "stabile."))
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
                                            message=_("""È disponibile una nuova versione stabile di School Life Diary. Ti 
                                            consigliamo di aggiornare il prima possibile per non perdere le nuove funzionalità, 
                                            i miglioramenti e le correzioni di problemi. Vuoi accedere alla pagina da cui 
                                            scaricare l'aggiornamento alla versione stabile {}?""").format(lp[0][1:]))
                    elif lp[0][0].lower() == "b" and bc == _("Sì"):
                        agg = tkmb.askyesno(title=_("Nuova versione BETA disponibile!"),
                                            message=_("""È disponibile una nuova versione BETA di School Life Diary. Queste 
                                            versioni non sono del tutto stabili e possono contenere alcuni problemi, 
                                            ma includono nuove funzionalità. Ricevi questo avviso poichè hai dato il tuo 
                                            consenso a ricevere le notifiche di versioni BETA Vuoi accedere alla pagina da 
                                            cui scaricare l'aggiornamento alla versione BETA {}?""").format(lp[0][1:]))
                    elif lp[0][0].lower() == "a" and ac == _("Sì"):
                        agg = tkmb.askyesno(title=_("Nuova versione ALPHA disponibile!"),
                                            message=_("""È disponibile una nuova versione ALPHA di School Life Diary. Queste 
                                            versioni non sono stabili e possono contenere parecchi problemi, ma includono nuove 
                                            funzionalità. Ricevi questo avviso poichè hai dato il tuo consenso a ricevere le 
                                            notifiche di nuove versioni ALPHA. Vuoi accedere alla pagina da cui scaricare 
                                            l'aggiornamento alla versione ALPHA {}?""").format(lp[0][1:]))
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
                                                 "Risposta non corretta della parte connessa dopo l'intervallo"
                                                 "di tempo oppure mancata risposta dall'host collegato. Riaprire l'app e"
                                                 "riprovare."))
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
