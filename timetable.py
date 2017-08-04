#Importazione di Tkinter
from tkinter import *
import tkinter.messagebox
#Creazione finestra
def creaFinestra():
    wt=Toplevel()
    wt.title("Orario scolastico - School Life Diary")
    wt.iconbitmap('sld_icon_beta.ico')
    wt.geometry("%dx%d+%d+%d" % (300, 300, 600, 250))
    ft=Frame(wt)
    ft.pack()
    l1=Label(text="Lunedì")
    l2=Label(text="Martedì")
    l3=Label(text="Mercoledì")
    l4=Label(text="Giovedì")
    l5=Label(text="Venerdì")
    l6=Label(text="Sabato")
    l1.grid(row=0, column=1)
    l2.grid(row=0, column=2)
    l3.grid(row=0, column=3)
    l4.grid(row=0, column=4)
    l5.grid(row=0, column=5)
    l6.grid(row=0, column=6)
    i=0
    x=1
    while (i<x):
        h=Button(text="")
        i+=1
    wt.mainloop()
