#Importazione di Tkinter
from tkinter import *
import tkinter.messagebox
import numpy as np
import os.path
def inizializza():
    global ds
    global dt
    ds=np.load('settings.npy').item()
    if not(os.path.exists(r"timetable.npy")):
        dt={}
        for x in range(1,ds["ORE_MAX_GIORNATA"]+1):
            for i in range (x,7):
                dt[[x,i]]=""
        np.save('timetable.npy', dt) 
    dt=np.load('timetable.npy').item()
#Creazione finestra
def creaFinestra():
    inizializza()
    wt=Toplevel()
    wt.title("Orario scolastico - School Life Diary")
    wt.iconbitmap('sld_icon_beta.ico')
    wt.geometry("%dx%d+%d+%d" % (400, 300, 600, 250))
    ft=Frame(wt)
    ft.pack()
    l1=Label(ft,text="Lunedì")
    l2=Label(ft,text="Martedì")
    l3=Label(ft,text="Mercoledì")
    l4=Label(ft,text="Giovedì")
    l5=Label(ft,text="Venerdì")
    l6=Label(ft,text="Sabato")
    l1.grid(row=0, column=1, pady=10, padx=5)
    l2.grid(row=0, column=2, pady=10, padx=5)
    l3.grid(row=0, column=3, pady=10, padx=5)
    l4.grid(row=0, column=4, pady=10, padx=5)
    l5.grid(row=0, column=5, pady=10, padx=5)
    l6.grid(row=0, column=6, pady=10, padx=5)
    i=1
    x=ds["ORE_MAX_GIORNATA"]
    while (i<x):
        h=Label(ft, text=str(i)+"° ora")
        h.grid(row=i, column=0, padx=5, pady=5)
        i+=1
    for c in range(1,x+1):
        for i in range(c,7):
            bh=Button(ft, text=dt[[c,i]], command=Cambiaorario)
        
    wt.mainloop()
