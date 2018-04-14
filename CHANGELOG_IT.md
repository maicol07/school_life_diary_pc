# Registro delle modifiche
Tutti i cambiamenti notabili verranno documentati in questo file

Questo formato è basato sul formato [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) e questo progetto aderisce al [Versionamento Semantico 2.0.0](https://semver.org/lang/it/).


## Non ancora rilasciato - Versione 1.0 (??/??/2018)

### Aggiunto

- Nuova sezione professori! Inserisci le info personali quali nome, cognome, immagine, sito web e email. Potrai poi collegarli alle loro materie!
- Aggiunte nuovi campi nelle materie.
- Temi! Possibilità di cambiare il tema visivo per l'app

### Cambiato

- Ridisegnata schermata iniziale
- Miglioramenti interfaccia delle schermate impostazioni e materie, ora viene visualizzata una tabella e un menu contestuale quando si usa il tasto destro.
- Miglioramenti grafici generali
- Cambiato database da file a SQLITE3

### Risolto

- Corretto problema durante lo scaricamento delle traduzioni dal server Transifex

### Rimosso

- Rimossa la funzionalità integrata di eliminazione dei dati direttamente dall'applicazione. Sarà necessario aprire manualmente la cartella dell'applicazione in Documenti\School Life Diary. Questo passaggio sarà ricordato anche quando si clicca sul pulsante CANCELLA TUTTO nelle Impostazioni. Probabilmente questa funzionalità ritornerà nella versione 1.1 della applicazione.


## Versione 0.3.0.1 (30/11/2017)

### Risolto
- Corretto problema su nuove installazioni: errore all'avvio a causa di file mancanti nell'installer della versione precedente.

## Versione 0.3 (18/10/2017):

### Aggiunto

- Gestione delle note (titolo, descrizione, file allegato (con apertura con doppio click)). Le note che contengono allegati se cliccate due volte visualizzeranno l'allegato.
- Nuova gestione delle traduzioni: oltre alle traduzioni locali, che vengono aggiornate ad ogni nuova versione del software, sarà possibile scaricarne delle nuove o aggiornare quelle esistenti manualmente mediante la finestra di cambio della lingua.

### Cambiato

- Ora le materie vengono automaticamente ordinate in ordine alfabetico.
- Miglioramenti grafici.

### Risolto

- Corretto il problema che causava l'errore all'avvio del programma quando si tenta di aprirlo senza internet. Il programma effettuava la ricerca degli aggiornamenti ma non avendo la connessione termina l'esecuzione. Ora il software verrà eseguito normalmente, ma mostrerà un avviso riguardante la mancanza della connessione.


## Versione 0.2.1 (02/09/2017)

### Aggiunto
- Aggiunto un nuovo menu nella home, con collegamenti rapidi e una nuova funzione di cambio della lingua
- Aggiunto il supporto alle lingue. Per ora disponibili solo Italiano (it) e Inglese (en)

### Cambiato
- Miglioramenti al codice e alla grafica


## Versione 0.2 (27/08/2017)

### Aggiunto
- Gestione delle materie con implementazione nell'orario
- Aggiunta possibilità di eseguire backup dei dati con relativo ripristino
- Aggiunta possibilità di cancellare tutto il database dell'applicazione (tutti i file che contengono dati dell'applicazione verranno cancellati, eccetto i backup). Questa funzione richiede 3 conferme per essere eseguita.
- Link all'agenda (in futuro verrà integrata nel software)
- Link alla sezione voti mobile (in futuro verrà integrata nel software)

### Cambiato
- Miglioramenti grafici: ora per gli utenti Windows verrà utilizzato il tema base della propria versione di Windows invece che il tema di Windows XP/2000; mentre per gli utenti MAC e Linux si utilizza il tema predefinito (aqua per i MAC)


## Versione 0.1 (11/08/2017)

### Aggiunto
- Prima beta con gestione completa dell'orario e impostazioni relative
