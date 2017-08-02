#####################
#                   #
#    SCHOOL LIFE    #
#       DIARY       #
#                   #
#    PC VERSION     #
#                   #
#####################

# Import tkinter
from tkinter import *
import tkinter.messagebox

#Functions

def b0():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b1():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b2():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b3():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def b4():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")
def bs():
    tkinter.messagebox.showwarning(title="Funzione non disponibile", message="LA FUNZIONE NON È ANCORA DISPONIBILE!")

#Window, frame and widgets creation
w=Tk()
w.title("School Life Diary")
w.iconbitmap('sld_icon_beta.ico')
f=Frame(w)
logo=PhotoImage(file=r"school_life_diary_splash.png")
title=Label(f,image=logo)
f.pack()
title.pack()
b0=Button(f,text="ORARIO", command=b0)
b1=Button(f,text="MATERIE", command=b1)
b2=Button(f,text="VOTI", command=b2)
b3=Button(f,text="NOTE", command=b3)
b4=Button(f,text="AGENDA", command=b4)
bs=Button(f,text="IMPOSTAZIONI", command=bs)
be=Button(f,text="ESCI", command=w.destroy)
b0.pack()
b1.pack()
b2.pack()
b3.pack()
b4.pack()
bs.pack()
be.pack()
#Run the window
w.mainloop()
