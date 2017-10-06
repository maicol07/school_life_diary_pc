#####################
#                   #
#    SCHOOL LIFE    #
#       DIARY       #
#                   #
#    PC VERSION     #
#                   #
#####################

#Inizializzazione impostazioni e creazione file
import gettext
import os
import ctypes
import locale
import PIL.Image, PIL.ImageTk
import os.path
import numpy as np
global pathset
import tkinter.messagebox
# filename for the file you want to save
output_filename = "settings.npy"

path = os.path.expanduser(r'~\Documents\School Life Diary')
# check the directory does not exist
if not(os.path.exists(path)):
    # create the directory you want to save to
    os.mkdir(path)
if not(os.path.exists(os.path.join(path,output_filename))):
    ds = {"ORE_MAX_GIORNATA": 5}
    # write the file in the new directory
    np.save(os.path.join(path, output_filename), ds)

#Selezione lingua

if not(os.path.exists(os.path.join(path,"language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode=locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lg = gettext.translation("main", localedir=os.path.join(path,'locale'), languages=[lgcode[0:2]])
else:
    try:
        fl=open(os.path.join(path,"language.txt"),"r")
        lgcode=fl.readline()
        lg = gettext.translation('main', localedir=os.path.join(path,'locale'), languages=[lgcode])
    except Exception as ex:
        tkinter.messagebox.showerror(title=_("Lingua non impostata!"),
                                     message=_(r"La lingua impostata non è stata riconosciuta. Per risolvere prova a eliminare il file in Documenti/School Life Diary/language.txt . Se il problema non si risolve, contattare lo sviluppatore. Errore: ")+str(ex))
lg.install()

# Importazione tkinter e funzioni utili
import webbrowser
from tkinter import *
from tkinter.ttk import Style, Progressbar
import settings
import subjects
import timetable
import note

#Funzioni
def info():
    wi=Toplevel()
    wi.configure(bg="white")
    wi.title(_("Informazioni")+" - School Life Diary")
    wi.iconbitmap("sld_icon_beta.ico")
    wi.geometry("750x450+250+50")
    f1=Frame(wi)
    f1.configure(bg="white")
    f1.pack()
    title=Label(f1,bg="white",text="School Life Diary", font=("Comic Sans MS",25,"bold italic"))
    title.pack(padx=10,pady=5)
    subtitle=Label(f1, text=_("sviluppato e mantenuto da maicol07"), bg="white")
    l1=Label(f1,text=_("Sito web: "), bg="white")
    bws=Button(f1, bg="white", text="https://apps.maicol07.tk",borderwidth=0,command=lambda: webbrowser.open("https://apps.maicol07.tk"))
    subtitle.pack(padx=10,pady=2)
    l1.pack(padx=10,pady=5)
    bws.pack(padx=10)
    l2=Label(f1,text=_("GitHub School Life Diary: "), bg="white")
    bgit=Button(f1, bg="white",text="https://github.com/maicol07/school_life_diary_pc",borderwidth=0, command=lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc"))
    l2.pack(padx=10,pady=5)
    bgit.pack(padx=10)
    l25=Label(f1, bg="white",text=_("Alcune icone fatte da Pixel Buddha di www.flaticon.com hanno licenza Creative Commons 3.0"))
    l25.pack(padx=10,pady=5)
    l3=Label(f1,text=_("Traduttori: "), bg="white")
    l3.pack(padx=10,pady=15)
    traduttori=Label(f1,text="maicol07", bg="white")
    traduttori.pack(padx=10,pady=10)
    l4=Label(f1,text=_("Vuoi diventare anche tu un traduttore?"), bg="white")
    bt=Button(f1, text=_("CLICCA QUI!"), command=lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc/wiki/Vuoi-diventare-traduttore-di-School-Life-Diary%3F"))
    l4.pack(padx=10,pady=15)
    bt.pack(padx=10)

#Creazione della finestra, del frame e dei widget
global w
#Verifica se esistono degli aggiornamenti per il programma
v="0.3"
import feedparser
from subprocess import check_output
feed_name="School Life Diary Releases"
url=r"https://github.com/maicol07/school_life_diary_pc/releases.atom"
feed=feedparser.parse(url)
wp=Tk()
wp.iconbitmap("images\sld_icon_beta.ico")
s=Style()
try:
    s.theme_use("vista")
except:
    s.theme_use()
pbv=0
le=Label(wp,text=_("Ricerca aggiornamenti..."))
le.pack(padx=10,pady=10)
pb=Progressbar(wp, mode="determinate",variable=pbv)
pb.pack(padx=10,pady=10)
def checknewversion(pb,wp):
    try:
        post=feed.entries[0]
        pb.step(20)
        title=post.title
        pb.step(20)
        lp=title.split(" ")
        pb.step(20)
        if (lp[0][1:].isdecimal()==True):
            lp[0]==lp[0][1:]
        pb.step(20)
        if (v!=lp[0][1:]):
            agg=tkinter.messagebox.askyesno(title=_("Nuova versione disponibile!"),
                                           message=_("È disponibile una nuova versione di School Life Diary.")+_("""
    Ti consigliamo di aggiornare il prima possibile per non perdere le novità, i miglioramenti e le correzioni di problemi.
    Vuoi accedere alla pagina da cui scaricare l'aggiornamento alla versione""")+" "+lp[0][1:]+"?")
            if (agg==True):
                webbrowser.open("https://github.com/maicol07/school_life_diary_pc/releases/")
        pb.step(20)
    except IndexError:
        tkinter.messagebox.showwarning(title=_("Nessuna connessione ad internet"),
                                       message=_("Non è disponibile nessuna connessione ad internet per la ricerca degli aggiornamenti. La ricerca verrà ritentata la prossima volta che sarà riaperto il programma."))
    wp.destroy()
wp.after(1,checknewversion(pb,wp))
wp.mainloop()
w=Tk()
w.configure(bg="white")
w.title("School Life Diary")
w.iconbitmap(r"images/sld_icon_beta.ico")
w.geometry("335x325+200+100")
mb=Menu(w)
w.config(menu=mb)
fm=Menu(mb,tearoff=0)
om=Menu(mb,tearoff=0)
hm=Menu(mb,tearoff=0)
iexit = PIL.Image.open("icons\exit.png")
pexit = PIL.ImageTk.PhotoImage(iexit)
isettings = PIL.Image.open("icons\settings.png")
psettings = PIL.ImageTk.PhotoImage(isettings)
ilanguage = PIL.Image.open("icons\language.png")
planguage = PIL.ImageTk.PhotoImage(ilanguage)
iguida = PIL.Image.open("icons\help1.png")
pguida = PIL.ImageTk.PhotoImage(iguida)
iinfo = PIL.Image.open("icons\help.png")
pinfo = PIL.ImageTk.PhotoImage(iinfo)
mb.add_cascade(label=_("File"),menu=fm)
fm.add_command(label=_("Esci"), image=pexit,
               compound="left",command=w.destroy)
mb.add_cascade(label=_("Opzioni"),menu=om)
om.add_command(label=_("Impostazioni"), image=psettings,
               compound="left", command=settings.creaFinestra)
om.add_command(label=_("Cambia lingua"), image=planguage,
               compound="left", command=settings.cambiaLingua)
mb.add_cascade(label=_("Aiuto"), menu=hm)
hm.add_command(label=_("Guida"), image=pguida,
               compound="left",
               command= lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc/wiki"))
hm.add_command(label=_("Informazioni"), image=pinfo,
               compound="left",command=info)
f=Frame(w)
f.configure(bg="white")
logo=PhotoImage(file=r"images/school_life_diary_splash.png")
title=Label(f,image=logo)
f.pack()
title.pack(padx=10,pady=10)
f2=Frame(w)
f2.configure(bg="white")
f2.pack()
itime = PIL.Image.open(r"icons\timetable.png")
ptime = PIL.ImageTk.PhotoImage(itime)
imaterie = PIL.Image.open(r"icons\subjects.png")
pmaterie = PIL.ImageTk.PhotoImage(imaterie)
ivoti = PIL.Image.open(r"icons\medal.png")
pvoti = PIL.ImageTk.PhotoImage(ivoti)
inote = PIL.Image.open(r"icons\notes.png")
pnote = PIL.ImageTk.PhotoImage(inote)
iagenda = PIL.Image.open(r"icons\agenda.png")
pagenda = PIL.ImageTk.PhotoImage(iagenda)
b0=Button(f2,text=_("ORARIO"), background="#FF6C6C", width=100, height=25, image=ptime,
          compound="left",
          command=timetable.creaFinestra)
b1=Button(f2,text=_("MATERIE"), background="#FFBD45", width=100, height=25, image=pmaterie,
          compound="left",
          command=subjects.creaFinestra)
b2=Button(f2,text=_("VOTI"), background="#ADD8E6", width=100, height=25, image=pvoti,
          compound="left", command=lambda: webbrowser.open('https://apps.maicol07.tk/app/sld/voti/'))
b3=Button(f2,text=_("ANNOTAZIONI"), background="#C389C3", width=100, height=25, image=pnote,
          compound="left", command=note.creaFinestra)
b4=Button(f2,text=_("AGENDA"), background="#7DFB7D", width=100, height=25, image=pagenda,
          compound="left", command=lambda: webbrowser.open('https://calendar.google.com'))
bs=Button(f2,text=_("IMPOSTAZIONI"), background="light grey", width=100, height=25, image=psettings,
          compound="left",
          command=settings.creaFinestra)
be=Button(f2,text=_("ESCI"), background="grey", width=100,image=pexit, height=25,
          compound="left",
          command=w.destroy)
b0.grid(row=0, column=0)
b1.grid(row=0, column=1)
b2.grid(row=0, column=2)
b3.grid(row=1, column=0)
b4.grid(row=1, column=1)
bs.grid(row=1, column=2)
be.grid(row=2, column=1)

#Avvia il programma
w.mainloop()
