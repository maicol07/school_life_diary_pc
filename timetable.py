#Importazione di Tkinter
from tkinter import *
import tkinter.messagebox
import numpy as np
import os.path

def Salvataggio(p,var):
    try:
        dt[p]=var.get()
        np.save('timetable.npy', dt)
        tkinter.messagebox.showinfo(title="Successo!", message="Salvataggio effettuato con successo!")
        wtc.destroy()
        wt.destroy()
        creaFinestra()
    except:
        tkinter.messagebox.showerror(title="Errore!", message="Si è verificato un errore, riprovare oppure contattare lo sviluppatore")

def CambiaOrario(p): #p è la posizione in coordinate y e x (tupla) del pulsante cliccato 
    global wtc
    wtc=Toplevel()
    wtc.title("Modifica Orario - Orario scolastico - School Life Diary")
    wtc.iconbitmap('sld_icon_beta.ico')
    wtc.geometry("%dx%d+%d+%d" % (450, 200, 600, 250))
    dg={1:"Lunedì",2:"Martedì",3:"Mercoledì",4:"Giovedì",5:"Venerdì",6:"Sabato"}
    l=Label(wtc, text="Inserire la materia da visualizzare nell'orario la "+str(p[1])+"a ora del "+dg[p[0]]+".")
    l.pack(padx=10,pady=10)
    var=StringVar(value="")
    e=Entry(wtc, textvariable=var)
    e.pack(padx=10,pady=10)
    b=Button(wtc, text="SALVA", command=lambda: Salvataggio(p,var))
    b.pack(padx=10,pady=10)
    wtc.mainloop()

def inizializza():
    global ds
    global dt
    ds=np.load('settings.npy').item()
    if not(os.path.exists(r"timetable.npy")):
        dt={}
        dt["ORE_MAX_GIORNATA"]=ds["ORE_MAX_GIORNATA"]
        for x in range(1,ds["ORE_MAX_GIORNATA"]+2):
            for i in range (1,7):
                dt[(x,i)]=""
        np.save('timetable.npy', dt) 
    dt=np.load('timetable.npy').item()
#Creazione finestra
def creaFinestra():
    inizializza()
    global wt
    wt=Toplevel()
    wt.title("Orario scolastico - School Life Diary")
    wt.iconbitmap('sld_icon_beta.ico')
    wt.geometry("%dx%d+%d+%d" % (600, 300, 600, 250))
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
    for i in range(1,x+1):
        h=Label(ft, text=str(i)+"° ora")
        h.grid(row=i, column=0, padx=5, pady=5)
        i+=1
    for c in range(1,x+2):
        for i in range(1, 7):
            bh=Button(ft, text=dt[(c,i)], width=10, command=lambda c=c,i=i: CambiaOrario((c,i)))
            bh.grid(row=i, column=c)
    wt.mainloop()
