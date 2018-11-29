#####################
#                   #
#    SCHOOL LIFE    #
#       DIARY       #
#                   #
#    PC VERSION     #
#                   #
#####################

print("CARICAMENTO IN CORSO...")
module_name = __name__.replace("_", "")
### START MAIN ###

import webbrowser
from tkinter import *
from tkinter.ttk import *

import PIL.Image
import PIL.ImageTk

from common import variables, init

path = variables.path

## IMPORTAZIONE MODULI APPLICAZIONE ##

from modules import settings, note, voti, timetable, subjects, agenda, prof

## INSTALLAZIONE LINGUA ##
lang = init.Language(module_name)

## CONNESSIONE AL DATABASE ##
conn, c = init.connect_database()

## CREAZIONE FINESTRA MENU PRINCIPALE ##
global w
w = Tk()
w.withdraw()
variables.style_init(c, w)
w.title("School Life Diary")
w.iconbitmap(r"images/school_life_diary.ico")


## FINESTRA INFORMAZIONI ##
def info():
    import codecs
    """
    Crea la finestra informazioni.

    Parametri
    ----------
    Nessuno

    Ritorna
    -------
    Niente
    """
    wi = Toplevel()
    wi.title(_("Informazioni") + " - School Life Diary")
    wi.iconbitmap(r"images\school_life_diary.ico")
    wi.geometry("850x750+250+50")
    f1 = Frame(wi)
    f1.pack()
    infotitle = Label(f1, text="School Life Diary", font=("Comic Sans MS", 25, "bold italic"))
    infotitle.pack()
    subtitle1 = Label(f1, text="{} Anniversary Update".format(variables.version),
                      font=("Times New Roman", 18, "bold italic"))
    subtitle1.pack()
    subtitle = Label(f1, text=_("sviluppato e mantenuto da maicol07"))
    subtitle.pack(padx=10, pady=2)
    framelinks = Labelframe(f1, text=_("Link"))
    framelinks.pack()
    bws = Button(framelinks, text=_("Sito web"), command=lambda: webbrowser.open("https://www.school-life-diary.tk"))
    bws.grid(row=0, column=0, padx=10, pady=5)
    bgit = Button(framelinks, text=_("Pagina del progetto su GitHub"),
                  command=lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc"))
    bgit.grid(row=0, column=1, padx=10, pady=5)
    bwsp = Button(framelinks, text=_("Sito web sviluppatore"),
                  command=lambda: webbrowser.open("https://www.maicol07.tk"))
    bwsp.grid(row=0, column=2, padx=10, pady=5)
    l25 = Label(f1, text=_("Si ringrazia Roundicons di flaticon.com per l'icona principale dell'applicazione, la quale "
                           "ha licenza Creative Commons BY 3.0.\nAlcune icone fatte da Pixel Buddha, Freepik, "
                           "Roundicons, Dimitry Miroliubov "
                           "e Smash Icons di www.flaticon.com hanno licenza Creative Commons BY 3.0"))
    l25.pack(padx=10, pady=5)
    l3 = Label(f1, text=_("Traduttori: "))
    l3.pack(padx=10, pady=5)
    traduttori = Label(f1, text="maicol07")
    traduttori.pack(padx=10, pady=5)
    l4 = Label(f1, text=_("Vuoi diventare anche tu un traduttore?"))
    bt = Button(f1, text=_("CLICCA QUI!"), command=lambda: webbrowser.open(
        "https://github.com/maicol07/school_life_diary_pc/wiki/Vuoi-diventare-traduttore-di-School-Life-Diary%3F"))
    l4.pack(padx=10, pady=5)
    bt.pack(padx=10)
    cl = Labelframe(wi, text=_("Registro delle modifiche"))
    cl.pack()
    changel = Text(cl, font="Courier 10", width=100, height=25)
    changel.pack()
    clf = codecs.open("CHANGELOG_{}.md".format(lang.lgcode.upper()[:2]), "r", "utf-8")
    for row in clf.readlines():
        changel.insert(INSERT, row)
    changel.config(state=DISABLED)


mb = Menu(w)
w.config(menu=mb)
fm = Menu(mb, tearoff=0)
om = Menu(mb, tearoff=0)
hm = Menu(mb, tearoff=0)
iexit = PIL.Image.open(r"icons\exit.png")
pexit = PIL.ImageTk.PhotoImage(iexit)
isettings = PIL.Image.open("icons\settings.png")
psettings = PIL.ImageTk.PhotoImage(isettings)
ilanguage = PIL.Image.open("icons\language.png")
planguage = PIL.ImageTk.PhotoImage(ilanguage)
iguida = PIL.Image.open("icons\help.png")
pguida = PIL.ImageTk.PhotoImage(iguida)
iinfo = PIL.Image.open("icons\info.png")
pinfo = PIL.ImageTk.PhotoImage(iinfo)
mb.add_cascade(label=_("File"), menu=fm)
fm.add_command(label=_("Esci"), image=pexit,
               compound="left", command=w.destroy)
mb.add_cascade(label=_("Opzioni"), menu=om)
om.add_command(label=_("Impostazioni"), image=psettings,
               compound="left", command=settings.creaFinestra)
om.add_command(label=_("Lingua"), image=planguage,
               compound="left", command=settings.cambiaLingua)
mb.add_cascade(label=_("Aiuto"), menu=hm)
hm.add_command(label=_("Guida"), image=pguida,
               compound="left",
               command=lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc/wiki"))
hm.add_command(label=_("Informazioni"), image=pinfo,
               compound="left", command=info)
f = Frame(w)
logo = PhotoImage(file=r"images/school_life_diary_splash.png")
title = Label(f, image=logo)
f.pack()
title.pack(padx=10, pady=10)
f2 = Frame(w)
f2.pack()
itime = PIL.Image.open(r"icons\timetable.png")
ptime = PIL.ImageTk.PhotoImage(itime)
imaterie = PIL.Image.open(r"icons\subjects.png")
pmaterie = PIL.ImageTk.PhotoImage(imaterie)
iprof = PIL.Image.open(r"icons\educator.png")
pprof = PIL.ImageTk.PhotoImage(iprof)
ivoti = PIL.Image.open(r"icons\medal.png")
pvoti = PIL.ImageTk.PhotoImage(ivoti)
inote = PIL.Image.open(r"icons\notes.png")
pnote = PIL.ImageTk.PhotoImage(inote)
iagenda = PIL.Image.open(r"icons\agenda.png")
pagenda = PIL.ImageTk.PhotoImage(iagenda)
bo = Button(f2, text=_("ORARIO"),  # background="#FF6C6C",
            style="TButton",
            image=ptime,
            compound="left",
            command=timetable.creaFinestra)
bm = Button(f2, text=_("MATERIE"),  # background="#FFBD45",
            image=pmaterie,
            compound="left",
            command=subjects.creaFinestra)
bp = Button(f2, text=_("PROFESSORI"),  # background="#7DFB7D",
            image=pprof,
            compound="left", command=prof.creaFinestra)
bv = Button(f2, text=_("VOTI"),  # background="#ADD8E6",
            image=pvoti,
            compound="left", command=voti.creaFinestra)
ban = Button(f2, text=_("ANNOTAZIONI"),  # background="#C389C3",
             image=pnote,
             compound="left", command=note.creaFinestra)
bag = Button(f2, text=_("AGENDA"),  # background="#7DFB7D",
             image=pagenda,
             compound="left", command=agenda.creaFinestra)
bo.grid(row=0, column=0, padx=5)
bm.grid(row=0, column=1, padx=5)
bp.grid(row=0, column=2, padx=5)
bv.grid(row=0, column=3, padx=5)
ban.grid(row=0, column=4, padx=5)
bag.grid(row=0, column=5, padx=5)
w.deiconify()
init.close_database(conn, c)
w.mainloop()
if "rFile" in globals():
    os.remove(rFile)
