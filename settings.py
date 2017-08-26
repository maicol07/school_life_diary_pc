#Importazione di Tkinter e librerie utili
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter.messagebox
import os.path #serve per verificare se un file è presente o no
import numpy as np #utility per il salvataggio delle impostazioni in un file .npy
from zipfile import *
import subprocess
import time
global path
global fn_set
fn_set = "settings.npy"
path = os.path.expanduser(r'~\Documents\School Life Diary')
def backup():
    fn_bk="backups"
    bfoldpath=os.path.join(path,fn_bk)
    if not(os.path.exists(os.path.join(path,fn_bk))):
        os.mkdir(os.path.join(path,fn_bk))
    bzip=ZipFile(os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip"),
                 "w",ZIP_DEFLATED)
    filelist = [ f for f in os.listdir(".") if f.endswith(".npy") ]
    for f in filelist:
        bzip.write(f, os.path.basename(f))
    bzip.close()
    subprocess.Popen(r'explorer /select,"'+os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip")+'"')
    tkinter.messagebox.showinfo(title="Backup effettuato!",
                                message="""Backup creato con successo!
Puoi trovare il backup nella cartella appena aperta o al seguente percorso del tuo computer: """+os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip"))
def ripristino():
    try:
        bkpath=filedialog.askopenfilename()
        bk=ZipFile(bkpath,"r")
        bk.extractall(path)
        bk.close()
        tkinter.messagebox.showinfo(title="Ripristino effettuato!",
                                    message="Backup ripristinato con successo! Riavvia per rendere effettive le modifiche!")
    except FileNotFoundError:
        return
    else:
        tkinter.messagebox.showerror(title="Ripristino non riuscito",
                                     message="Purtroppo il ripristino non è riuscito. Riprova, anche con un backup diverso, oppure contattare lo sviluppatore.")
def cancellatutto():
    for i in range(3):
        sc=tkinter.messagebox.askyesno(title="Conferma n."+str(i),
                                    message="""Sei sicuro di voler eliminare TUTTI i dati presenti nell'applicazione?
Questo include:
- Orario
- Materie
- Voti (no online)
- Note
- Agenda (no Google Calendar online)
- Impostazioni.\n
NON potrai più recuperare i tuoi dati se vai avanti a meno che non abbia effettuato un backup precedentemente.
Conferme rimaste prima dell'eliminazione: """+str(3-i))
        if sc==False:
            return
    filelist = [ f for f in os.listdir(".") if f.endswith(".npy") ]
    for f in filelist:
        os.remove(f)
    ws.destroy()
    tkinter.messagebox.showinfo(title="Dati cancellati correttamente",
                                message="Tutti i tuoi dati sono stati cancellati con successo! Riavvia l'applicazione per non riscontrare errori!")
def salvataggio0():
    try:
        ds["ORE_MAX_GIORNATA"]=int(sv.get())
        np.save(os.path.join(path, fn_set), ds) 
        tkinter.messagebox.showinfo(title="Successo!",
                                    message="Parametro modificato con successo! RICORDATI DI RIAVVIARE L'APPLICAZIONE PER RENDERE EFFETTIVE LE MODIFICHE!!")
        wcv.destroy()
        v0["text"]=ds["ORE_MAX_GIORNATA"]
        global new_set0
        new_set0=True
    except:
        tkinter.messagebox.showerror(title="ERRORE!", message="Si è verificato un errore durante la modifica del parametro. Riprovare o contattare lo sviluppatore!")
def accept_whole_number_only(e=None):
    value = sv.get()
    if int(value) != value:
        sv.set(round(value))
        
def cambiaValore0():
    global wcv
    wcv=Toplevel()
    wcv.title("Cambia valore - Impostazioni - School Life Diary")
    wcv.iconbitmap("sld_icon_beta.ico")
    wcv.geometry("%dx%d+%d+%d" % (400, 200, 600, 250))
    etichetta1=Label(wcv, text="Sceglere il valore da attribuire al parametro:")
    var=IntVar()
    global sv
    sv=Scale(wcv, variable=var, from_=4, to=8, orient=HORIZONTAL, command=accept_whole_number_only)
    lvar=Label(wcv, textvariable=var)
    bt1=Button(wcv,text="SALVA", command=salvataggio0)
    etichetta1.pack(padx=10, pady=10)
    lvar.pack(padx=10, pady=2)
    sv.pack(padx=10, pady=10)
    bt1.pack(padx=10, pady=10)
    wcv.mainloop()
    
def inizializza():
    global ds
    ds=np.load(os.path.join(path, fn_set)).item()
    v0["text"]=ds["ORE_MAX_GIORNATA"]
#Creazione finestra
def creaFinestra():
    s=Style()
    try:
        s.theme_use("vista")
    except:
        s.theme_use()
    global ws
    ws=Toplevel()
    ws.title("Impostazioni - School Life Diary")
    ws.iconbitmap("sld_icon_beta.ico")
    ws.geometry("%dx%d+%d+%d" % (900, 400, 600, 250))
    fs=Frame(ws)
    fs.pack()
    la1=Label(fs,text="Parametro")
    la2=Label(fs,text="Valore attuale")
    la3=Label(fs,text="Descrizione")
    la4=Label(fs,text="Azioni")
    la1.grid(row=0, column=0, padx=10, pady=10)
    la2.grid(row=0, column=1, padx=10, pady=10)
    la3.grid(row=0, column=2, padx=10, pady=10)
    la4.grid(row=0, column=3, padx=10, pady=10)
    p0=Label(fs,text="ORE_MAX_GIORNATA")
    global v0
    v0=Label(fs,text="5")
    d0=Label(fs,text="Imposta il numero di ore massime per giornate da visualizzare nell'orario")
    a0=Button(fs,text="Cambia", command=cambiaValore0)
    p0.grid(row=1, column=0, padx=10, pady=10)
    v0.grid(row=1, column=1, padx=10, pady=10)
    d0.grid(row=1, column=2, padx=10, pady=10)
    a0.grid(row=1, column=3, padx=10, pady=10)
    fbr=Frame(ws)
    bb=Button(fbr,text="ESEGUI BACKUP",command=backup)
    br=Button(fbr,text="ESEGUI RIPRISTINO",command=ripristino)
    bc=Button(fbr,text="CANCELLA TUTTO",command=cancellatutto)
    fbr.pack()
    bb.grid(row=0,column=0,padx=10,pady=10)
    br.grid(row=0,column=1,padx=10,pady=10)
    bc.grid(row=0,column=2,padx=10,pady=10)
    inizializza()
    ws.mainloop()
