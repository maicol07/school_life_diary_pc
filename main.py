#####################
#                   #
#    SCHOOL LIFE    #
#       DIARY       #
#                   #
#    PC VERSION     #
#                   #
#####################

# Importazione tkinter e funzioni utili
from tkinter import *
import tkinter.messagebox
import settings
import timetable

#Funzioni

def b0():
    timetable.creaFinestra()
def b1():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b2():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b3():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b4():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def bs():
    settings.creaFinestra()

#Creazione della finestra, del frame e dei widget
w=Tk()
w.title("School Life Diary")
w.iconbitmap('sld_icon_beta.ico')
w.geometry("%dx%d+%d+%d" % (325, 325, 200, 100))
f=Frame(w)
logo=PhotoImage(file=r"school_life_diary_splash.png")
title=Label(f,image=logo)
f.pack()
title.pack()
blank=Label(f)
blank.pack()
f2=Frame(w)
f2.pack()
b0=Button(f2,text="ORARIO", background="red", width=13, command=b0)
b1=Button(f2,text="MATERIE", background="orange", width=13, command=b1)
b2=Button(f2,text="VOTI", background="cyan", width=13, command=b2)
b3=Button(f2,text="NOTE", background="purple", width=13, command=b3)
b4=Button(f2,text="AGENDA", background="green", width=13, command=b4)
bs=Button(f2,text="IMPOSTAZIONI", background="light blue", width=13, command=bs)
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
