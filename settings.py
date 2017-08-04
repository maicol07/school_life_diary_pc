#Importazione di Tkinter
from tkinter import *
import tkinter.messagebox
#Creazione finestra
def creaFinestra():
    ws=Toplevel()
    ws.title("Impostazioni - School Life Diary")
    ws.iconbitmap('sld_icon_beta.ico')
    ws.geometry("%dx%d+%d+%d" % (400, 400, 600, 250))
    fs=Frame(ws)
    fs.pack()
    la1=Label(fs,text="Parametro")
    la2=Label(fs,text="Valore attuale")
    la3=Label(fs,text="Descrizione")
    la4=Label(fs,text="Azioni")
    la1.grid(row=0, column=0)
    la2.grid(row=0, column=1)
    la3.grid(row=0, column=2)
    la4.grid(row=0, column=3)
    p1=Label(fs,text="ORE_MAX_GIORNATA")
    v1=Label(fs,text="5")
    d1=Label(fs,text="Imposta il numero di ore massime per giornate da visualizzare nell'orario")
    a1=Button(fs,text="Cambia")
    p1.grid(row=1, column=0)
    v1.grid(row=1, column=1)
    d1.grid(row=1, column=2)
    a1.grid(row=1, column=3)
    ws.mainloop()
