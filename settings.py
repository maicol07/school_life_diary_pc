#Importazione di Tkinter e librerie utili
from transifex.api import TransifexAPI
global tr
tr = TransifexAPI('sld', 'sld2017', 'https://www.transifex.com')
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
import gettext
import ctypes
import locale
import polib
if not(os.path.exists(os.path.join(path,"language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode=locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lgl=["en","it"]
    lg = gettext.translation("settings", localedir=os.path.join(path,'locale'), languages=[lgcode[0:2]])
else:
    fl=open(os.path.join(path,"language.txt"),"r")
    lgcode=fl.readline()
    lg = gettext.translation('settings', localedir=os.path.join(path,'locale'), languages=[lgcode])
    fl.close()
lg.install()

def salvaLingua(cb,lgl,wl,mode):
    try:
        if mode=="download":
            l=["main","settings","note","timetable","subject"]
            for i in l:
                lang=tr.list_languages('school-life-diary-pc', i+"pot")
                for y in lang:
                    pathdl=os.path.join(path,'locale',y[:2],"LC_MESSAGES")
                    if not(os.path.exists(os.path.join(pathdl,(i+'.po')))):
                        if not(os.path.exists(os.path.join(pathdl))):
                            os.makedirs(os.path.join(pathdl))
                        filecreation=open(os.path.join(pathdl,(i+'.po')), "w")
                        filecreation.close()
                    tr.get_translation('school-life-diary-pc', i+"pot", 'pt-br', os.path.join(pathdl,(i+'.po')))
                    po = polib.pofile(os.path.join(pathdl,(i+'.po')))
                    po.save_as_mofile(os.path.join(pathdl,(i+'.mo')))
        else:
            f=open(os.path.join(path,"language.txt"),"w")
            f.write(lgl[cb.get()])
            f.close()
        tkinter.messagebox.showinfo(title=_("Salvataggio effettuato"),
                                message=_("La lingua scelta è stata salvata. RIAVVIA L'APPLICAZIONE PER RENDERE EFFETTIVE LE MODIFICHE!"))
    except Exception as ex:
        if str(ex)=="404: b'Not Found'":
            updatecb(cb,lgl)
            tkinter.messagebox.showinfo(title=_("Lingue scaricate"),
                                message=_("La lingue sono state scaricate. Puoi sceglierne una dal menu!"))
        else:
            tkinter.messagebox.showerror(title=_("Si è verificato un errore!!"),
                                        message=_("È stato riscontrato un errore imprevisto. Riprovare o contattare lo sviluppatore.")+"\n"+str(ex))
    wl.destroy()
def updatecb(cb,lgl):
    cb["values"]=lgl
def cambiaLingua():
    wl=Toplevel()
    wl.title(_("Cambia lingua")+" - School Life Diary")
    wl.iconbitmap("sld_icon_beta.ico")
    wl.geometry("500x250+100+100")
    lgl=os.listdir(os.path.join(path, "locale"))
    e1=Label(wl,text=_("Scegliere la propria lingua: "))
    cb=Combobox(wl,postcommand=lambda: updatecb(cb,lgl))
    e1.pack(padx=10,pady=10)
    cb.pack(padx=10,pady=10)
    btn=Button(wl,text=_("CAMBIA"),command=lambda: salvaLingua(cb,lgl,wl,"change"))
    btn.pack(padx=10,pady=10)
    l=Label(wl,text=_("Scarica lingue non presenti nella lista\n o aggiorna quelle esistenti dalla nostra piattaforma di traduzione."))
    l.pack(padx=10,pady=2)
    btn1=Button(wl,text=_("SCARICA O AGGIORNA LINGUE"), command=lambda: salvaLingua(cb, lgl, wl, "download"))
    btn1.pack(padx=5,pady=10)
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
    tkinter.messagebox.showinfo(title=_("Backup effettuato!"),
                                message=_("""Backup creato con successo!
Puoi trovare il backup nella cartella appena aperta o al seguente percorso del tuo computer: """)+os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip"))
def ripristino():
    try:
        bkpath=filedialog.askopenfilename()
        bk=ZipFile(bkpath,"r")
        bk.extractall(path)
        bk.close()
        tkinter.messagebox.showinfo(title=_("Ripristino effettuato!"),
                                    message=_("Backup ripristinato con successo! Riavvia per rendere effettive le modifiche!"))
    except FileNotFoundError:
        return
    except Exception as ex:
        tkinter.messagebox.showerror(title=_("Ripristino non riuscito"),
                                     message=_("Purtroppo il ripristino non è riuscito. Riprova, anche con un backup diverso, oppure contattare lo sviluppatore.")+"\n"+ex)
def cancellatutto():
    for i in range(3):
        sc=tkinter.messagebox.askyesno(title=_("Conferma n.")+str(i),
                                    message=_("""Sei sicuro di voler eliminare TUTTI i dati presenti nell'applicazione?
Questo include:
- Orario
- Materie
- Voti (no online)
- Note
- Agenda (no Google Calendar online)
- Impostazioni
NON potrai più recuperare i tuoi dati se vai avanti a meno che non abbia effettuato un backup precedentemente.
Conferme rimaste prima dell'eliminazione: """)+str(3-i))
        if sc==False:
            return
    filelist = [ f for f in os.listdir(".") if f.endswith(".npy") ]
    for f in filelist:
        os.remove(f)
    ws.destroy()
    tkinter.messagebox.showinfo(title=_("Dati cancellati correttamente"),
                                message=_("Tutti i tuoi dati sono stati cancellati con successo! Riavvia l'applicazione per non riscontrare errori!"))
def salvataggio0():
    try:
        ds["ORE_MAX_GIORNATA"]=int(sv.get())
        np.save(os.path.join(path, fn_set), ds) 
        tkinter.messagebox.showinfo(title=_("Successo!"),
                                    message=_("Parametro modificato con successo! RICORDATI DI RIAVVIARE L'APPLICAZIONE PER RENDERE EFFETTIVE LE MODIFICHE!!"))
        wcv.destroy()
        v0["text"]=ds["ORE_MAX_GIORNATA"]
        global new_set0
        new_set0=True
    except:
        tkinter.messagebox.showerror(title=_("ERRORE!"),
                                     message=_("Si è verificato un errore durante la modifica del parametro. Riprovare o contattare lo sviluppatore!"))
def accept_whole_number_only(e=None):
    value = sv.get()
    if int(value) != value:
        sv.set(round(value))
        
def cambiaValore0():
    global wcv
    wcv=Toplevel()
    wcv.title(_("Cambia valore - Impostazioni")+" - School Life Diary")
    wcv.iconbitmap("sld_icon_beta.ico")
    wcv.geometry("400x200+600+250")
    etichetta1=Label(wcv, text=_("Sceglere il valore da attribuire al parametro:"))
    var=IntVar()
    global sv
    sv=Scale(wcv, variable=var, from_=4, to=8, orient=HORIZONTAL, command=accept_whole_number_only)
    lvar=Label(wcv, textvariable=var)
    bt1=Button(wcv,text=_("SALVA"), command=salvataggio0)
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
    ws.title(_("Impostazioni")+" - School Life Diary")
    ws.iconbitmap("sld_icon_beta.ico")
    ws.geometry("900x400+600+250")
    fs=Frame(ws)
    fs.pack()
    la1=Label(fs,text=_("Parametro"))
    la2=Label(fs,text=_("Valore attuale"))
    la3=Label(fs,text=_("Descrizione"))
    la4=Label(fs,text=_("Azioni"))
    la1.grid(row=0, column=0, padx=10, pady=10)
    la2.grid(row=0, column=1, padx=10, pady=10)
    la3.grid(row=0, column=2, padx=10, pady=10)
    la4.grid(row=0, column=3, padx=10, pady=10)
    p0=Label(fs,text="ORE_MAX_GIORNATA")
    global v0
    v0=Label(fs,text="5")
    d0=Label(fs,text=_("Imposta il numero di ore massime per giornate da visualizzare nell'orario"))
    a0=Button(fs,text=_("Cambia"), command=cambiaValore0)
    p0.grid(row=1, column=0, padx=10, pady=10)
    v0.grid(row=1, column=1, padx=10, pady=10)
    d0.grid(row=1, column=2, padx=10, pady=10)
    a0.grid(row=1, column=3, padx=10, pady=10)
    fbr=Frame(ws)
    bb=Button(fbr,text=_("ESEGUI BACKUP"),command=backup)
    br=Button(fbr,text=_("ESEGUI RIPRISTINO"),command=ripristino)
    bc=Button(fbr,text=_("CANCELLA TUTTO"),command=cancellatutto)
    fbr.pack()
    bb.grid(row=0,column=0,padx=10,pady=10)
    br.grid(row=0,column=1,padx=10,pady=10)
    bc.grid(row=0,column=2,padx=10,pady=10)
    inizializza()
    ws.mainloop()
