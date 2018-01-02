#IMPORTAZIONE LIBRERIE E IMPOSTAZIONE CLIENT TRADUZIONI
from transifex.api import TransifexAPI
global tr
tr = TransifexAPI('sld', 'sld2017', 'https://www.transifex.com')
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, Tk, Toplevel
import tkinter.messagebox as tkmb
import os.path #serve per verificare se un file è presente o no
from zipfile import *
import subprocess, time, gettext, ctypes, locale, polib
import sqlite3 as sql
global path
global fn_set

# VARIABILI D'AMBIENTE
fn_set = "settings.db"
path = os.path.expanduser(r'~\Documents\School Life Diary')
conn=sql.connect(os.path.join(path, fn_set), isolation_level=None)
c=conn.cursor()

# INSTALLAZIONE LINGUA
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



# SALVATAGGIO LINGUA
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
        tkmb.showinfo(title=_("Salvataggio effettuato"),
                                message=_("La lingua scelta è stata salvata. RIAVVIA L'APPLICAZIONE PER RENDERE EFFETTIVE LE MODIFICHE!"))
    except Exception as ex:
        if str(ex)=="404: b'Not Found'":
            updatecb(cb,lgl)
            tkmb.showinfo(title=_("Lingue scaricate"),
                                message=_("La lingue sono state scaricate. Puoi sceglierne una dal menu!"))
        else:
            tkmb.showerror(title=_("Si è verificato un errore!!"),
                                        message=_("È stato riscontrato un errore imprevisto. Riprovare o contattare lo sviluppatore.")+"\n"+str(ex))
    wl.destroy()


# AGGIORNAMENTO LISTA LINGUE
def updatecb(cb,lgl):
    cb["values"]=lgl


# CAMBIO LINGUA
def cambiaLingua():
    wl=Toplevel()
    wl.configure(background="white")
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

# BACKUP DEI DATABASE
def backup():
    fn_bk="backups"
    bfoldpath=os.path.join(path,fn_bk)
    if not(os.path.exists(os.path.join(path,fn_bk))):
        os.mkdir(os.path.join(path,fn_bk))
    bzip=ZipFile(os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip"),
                 "w",ZIP_DEFLATED)
    filelist = [ f for f in os.listdir(".") if f.endswith(".db") ]
    for f in filelist:
        bzip.write(f, os.path.basename(f))
    bzip.close()
    subprocess.Popen(r'explorer /select,"'+os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip")+'"')
    tkmb.showinfo(title=_("Backup effettuato!"),
                                message=_("""Backup creato con successo!
Puoi trovare il backup nella cartella appena aperta o al seguente percorso del tuo computer: """)+os.path.join(path,
                              fn_bk,
                              "backup-"+time.strftime("%d-%m-%Y")+"-"+time.strftime("%H-%M-%S")+".zip"))


# RIPRISTINO DEI DATI DA BACKUP
def ripristino():
    try:
        bkpath=filedialog.askopenfilename()
        bk=ZipFile(bkpath,"r")
        bk.extractall(path)
        bk.close()
        tkmb.showinfo(title=_("Ripristino effettuato!"),
                                    message=_("Backup ripristinato con successo! Riavvia per rendere effettive le modifiche!"))
    except FileNotFoundError:
        return
    except Exception as ex:
        tkmb.showerror(title=_("Ripristino non riuscito"),
                                     message=_("Purtroppo il ripristino non è riuscito. Riprova, anche con un backup diverso, oppure contattare lo sviluppatore.")+"\n"+ex)


# ELIMINAZIONE DI TUTTI I DATI
def cancellatutto():
    for i in range(3):
        sc=tkmb.askyesno(title=_("Conferma n.")+str(i),
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
    filelist = [ f for f in os.listdir(".") if f.endswith(".db") ]
    for f in filelist:
        os.remove(f)
    ws.destroy()
    tkmb.showinfo(title=_("Dati cancellati correttamente"),
                                message=_("Tutti i tuoi dati sono stati cancellati con successo! Riavvia l'applicazione per non riscontrare errori!"))

# Salvataggio impostazioni
def salvaImpostazioni(par,val):
    try:
        if par=="ORE_MAX_GIORNATA":
            c.execute("""UPDATE settings SET value = {} WHERE setting='{}';""".format(str(int(val.get())),par))
        else:
            c.execute("""UPDATE settings SET value = '{}' WHERE setting='{}';""".format(val.get(),par))            
        tkmb.showinfo(title=_("Successo!"),
                                    message=_("Parametro modificato con successo!\n\nRICORDATI DI RIAVVIARE L'APPLICAZIONE PER RENDERE EFFETTIVE LE MODIFICHE!!"))
        wcv.destroy()
        ws.destroy()
        global new_set0
        new_set0=True
        creaFinestra()
    except Exception as ex:
        tkmb.showerror(title=_("ERRORE!"),
                                     message=_("Si è verificato un errore durante la modifica del parametro. Riprovare o contattare lo sviluppatore! Errore riscontrato:\n")+str(ex))

# ACCETTAZIONE SOLO VALORI INTERI NELLO SLIDER
def accept_whole_number_only(sv,e=None):
    value = sv.get()
    if int(value) != value:
        sv.set(int(round(value)))


# INIZIALIZZAZIONE IMPOSTAZIONI
def inizializza():
    global ds
    ds={}
    c.execute("SELECT * FROM settings")
    sr=c.fetchall()
    for row in sr:
        ds[row[0]]=(row[1],row[2])

    
# MODIFICA VALORE DEL PARAMETRO
def modifica_valore(event):
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    par = item['values'][0]
    global wcv
    wcv=Toplevel()
    wcv.configure(background="white")
    wcv.title(_("Cambia valore - Impostazioni")+" - School Life Diary")
    wcv.iconbitmap("sld_icon_beta.ico")
    wcv.geometry("400x200+600+250")
    etichetta1=Label(wcv, text=_("Scegliere il valore da attribuire al parametro:"))
    etichetta1.pack(padx=10, pady=10)
    if par=="ORE_MAX_GIORNATA":
        var=IntVar()
        var.set(4)
        sv=Scale(wcv, variable=var, from_=4, to=8, orient=HORIZONTAL, command=lambda e: accept_whole_number_only(sv))
        lvar=Label(wcv, textvariable=var)
        lvar.pack(padx=10, pady=2)
        sv.pack(padx=10, pady=10)
        bts=Button(wcv,text=_("SALVA"), command=lambda: salvaImpostazioni(par,sv))
    if par=="PC_THEME":
        menut=Combobox(wcv,postcommand=lambda: updateList(menut,Style().theme_names()))
        menut.pack(padx=10,pady=10)
        bts=Button(wcv,text=_("SALVA"), command=lambda: salvaImpostazioni(par,menut))
    bts.pack(padx=10, pady=10)
    wcv.focus()
    wcv.mainloop()
    
# IMPOSTAZIONE ELEMENTI MENU A TENDINA
def updateList(menut,l):
    menut["values"]=l


# CREAZIONE FINESTRA
def creaFinestra():
    inizializza()
    s=Style()
    s.theme_use(c.execute("SELECT value FROM settings WHERE setting='PC_THEME'").fetchone())
    s.configure("TFrame",background="white")
    s.configure("TLabelframe",background="white")
    s.configure("TLabel",background="white")
    s.configure("TLabelframe.Label",background="white")
    s.configure("TScale",background="white")
    global ws
    ws=Toplevel()
    ws.configure(bg="white")
    ws.title(_("Impostazioni")+" - School Life Diary")
    ws.iconbitmap("sld_icon_beta.ico")
    ws.geometry("900x400+600+250")
    fs=Labelframe(ws,text=_("Parametri"))
    fs.pack()
    ts=Treeview(fs)
    ts["columns"]=("par","val_att","descr")
    ts.heading("#0",text=_("ID"))
    ts.column("#0",width=30)
    ts.heading("par",text=_("Parametro"),anchor=CENTER)
    ts.column("par",anchor=CENTER)
    ts.heading("val_att",text=_("Valore attuale"))
    ts.column("val_att",anchor=CENTER)
    ts.heading("descr",text=_("Descrizione"))
    ts.column("descr",width=450,anchor=CENTER)
    ts.bind("<Double-Button-1>", modifica_valore)
    ts.pack()
    for x in range(len(list(ds))):
        e=ds[list(ds.keys())[x]]
        ts.insert("","end",text=x,values=[list(ds.keys())[x],e[0],e[1]])
    li=Label(ws,text=_("Per modificare un parametro, fai doppio click sulla riga corrispondente."))
    li.pack()
    fbr=Labelframe(ws,text=_("Backup & Ripristino"))
    bb=Button(fbr,text=_("ESEGUI BACKUP"),command=backup)
    br=Button(fbr,text=_("ESEGUI RIPRISTINO"),command=ripristino)
    bc=Button(fbr,text=_("CANCELLA TUTTO"),command=cancellatutto)
    fbr.pack()
    bb.grid(row=0,column=0,padx=10,pady=10)
    br.grid(row=0,column=1,padx=10,pady=10)
    bc.grid(row=0,column=2,padx=10,pady=10)
    ws.focus()
    ws.mainloop()
    c.close()
