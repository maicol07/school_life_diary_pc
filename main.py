#####################
#                   #
#    SCHOOL LIFE    #
#       DIARY       #
#                   #
#    PC VERSION     #
#                   #
#####################

#Inizializzazione impostazioni e creazione file
import os.path
import numpy as np
global pathset
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

# Importazione tkinter e funzioni utili
from tkinter import *
from tkinter.ttk import Style
import tkinter.messagebox
import settings
import subjects
import timetable

#Funzioni

def b3():
    tkinter.messagebox.showwarning(title="Funzione non disponibile",
                                   message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b2():
    import webbrowser
    webbrowser.open('https://apps.maicol07.tk/app/sld/voti/')
def b4():
    import webbrowser
    webbrowser.open('https://calendar.google.com')

#Creazione della finestra, del frame e dei widget
w=Tk()
w.title("School Life Diary")
w.iconbitmap("sld_icon_beta.ico")
w.geometry("%dx%d+%d+%d" % (325, 325, 200, 100))
s=Style()
try:
    s.theme_use("vista")
except:
    s.theme_use()
f=Frame(w)
logo=PhotoImage(file=r"school_life_diary_splash.png")
title=Label(f,image=logo)
f.pack()
title.pack()
blank=Label(f)
blank.pack()
f2=Frame(w)
f2.pack()
b0=Button(f2,text="ORARIO", background="#FF6C6C", width=13,
          command=timetable.creaFinestra)
b1=Button(f2,text="MATERIE", background="#FFBD45", width=13,
          command=subjects.creaFinestra)
b2=Button(f2,text="VOTI", background="#ADD8E6", width=13, command=b2)
b3=Button(f2,text="NOTE", background="#C389C3", width=13, command=b3)
b4=Button(f2,text="AGENDA", background="#7DFB7D", width=13, command=b4)
bs=Button(f2,text="IMPOSTAZIONI", background="light grey", width=13,
          command=settings.creaFinestra)
be=Button(f2,text="ESCI", background="grey", width=13, command=w.destroy)
b0.grid(row=0, column=0)
b1.grid(row=0, column=1)
b2.grid(row=0, column=2)
b3.grid(row=1, column=0)
b4.grid(row=1, column=1)
bs.grid(row=1, column=2)
be.grid(row=2, column=1)
#Avvia il programma
w.mainloop()
