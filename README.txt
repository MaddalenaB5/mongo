# README per app MongoDB TicketTwo

# DESCRIZIONE

Questa è una applicazione pc per poter comprare biglietti per concerti. L'app utilizza un database MongoDB per poter salvare e recuperare le informazioni sugli eventi, sugli artisti e sulle location. 

# FUNZIONI

L'app permette all'utente di poter scegliere e comprare biglietti per eventi e concerti. Gli eventi, gli artisti e le location sono tutte caricate nel database MongoDB come JSON. L'utente può fare una ricerca in base alle proprie preferenze, in particolare può scegliere se cercare:
	- per nome dell'artista (solitamente il nome d'arte, o del gruppo)
	- per location, fornendo le coordinate da cui effettuare la ricerca per un raggio di 7km
	- per nome dell'evento
	- per periodo, fornendo una data di inizio e di fine
Una volta effettuata la ricerca, l'utente riceverà un menu per poter scegliere l'artista/la location/il periodo preferita e poi l'evento per cui vuole comprare i biglietti. Una volta selezionato, l'utente può scegliere quanti biglietti comprare, e gli verrà fornito il costo totale e il codice identificativo dei biglietti. 
Terminato l'acquisto, l'utente ritornerà al menu principale, dove potrà effettuare un'altra ricerca, o chiudere l'applicazione.

# APPLICAZIONI USATE

- MongoDB Server
- Python:
	- libreria time
	- libreria pymongo
	- libreria datetime

N.B. Le librerie da installare sono inserite nel file requirements.txt

# INSTALLAZIONE

Per poter usare l'applicazione è necessario disporre di Python 3.

Per installare l'app è necessario scaricare la repo di GitHub al link
https://github.com/MaddalenaB5/mongo

Bisogna aprire la cartella 'Repository Data Lake' e aprire con un qualunque IDE il file GUI.py
Dopo essersi assicurati dell'installazione delle librerie necessarie, è sufficiente far partire il codice
di GUI.py per poter far partire la chat. 

N.B. Una connessione ad internet è necessaria per poter usare l'app, dato che l'utente deve poter accedere al
server MongoDB. Risulta possibile cambiare il server modificando l'indirizzo e il nome del database nel codice.

# COME USARE L'APPLICAZIONE

L'applicazione funziona da terminale, per cui l'utente deve disporre di un IDE per Python. Una clonata la cartella, l'utente deve lanciare il file file_lavoro.py. Sulla console comparirà il menu principale con le opzioni di ricerca (a - artista, d - date, e - evento, v - vicinanza/location, x - chiusura applicazione). Le ricerche permettono l'accesso alla ricerca, ognuna effettuata in maniera differente:
	- la ricerca per artista chiede all'utente il nome d'arte dell'artista e fa una ricerca, anche parziale 
	  del nome dell'artista
	- la ricerca per date chiede all'utente di inserire due date (se l'utente vuole selezionare una sola data, 	  deve inserire la stessa data due volte) in formato AAAA-MM-GG. Verrà effettuata una ricerca per tutti 
	  gli eventi che accadono in quel periodo.
	- la ricerca per evento chiede all'utente il nome dell'evento e fa una ricerca, anche parziale per il nome
	  dell'evento
	- la ricerca per vicinanza chiede all'utente di inserire la latitudine e la longitudine da cui effettuare
	  la ricerca e trova tutte le location in un raggio di 7km dall'origine
Una volta effettuata la ricerca, viene chiesto all'utente di selezionare la propria preferenza e l'evento cercato. Dopodiché l'utente ha la possibilità di acquistare biglietti per l'evento, acquistandone anche più di uno. In caso siano disponibili, verranno stampati i codici identificativi dei biglietti e il prezzo totale. 
Terminata la ricerca l'utente ritorna al menu principale e può chiudere l'applicazione o effettuare un'altra ricerca e comprare altri biglietti. 

# NOTE

--- disclaimer 
L'app è stata creata come progetto scolastico per l'ITS Angelo Rizzoli di Milano, corso Big Data Specialist classe 2023-25. L'app è stata creata col contributo degli studenti Bozzola Maddalena, Berganton Federico, Durante Pierluigi e Rutigliano Denny. 


--- svolgimento del progetto
La prima parte del progetto è stata la creazione dei JSON per il database MongoDB. Abbiamo deciso di creare tre collezioni: artisti, eventi e locations, ognuna contente informazioni differenti.
La collezione artisti è composta da oggetti del tipo:     
{ 
        "_id": "A1",
        "artista": {"nome_arte": "Ligabue", "nome": "Luciano", "cognome": "Ligabue"},
        "lista_eventi": ["E31"]
}
La collezione eventi è composta da oggetti del tipo:
{  
        "_id": "E1",
       "nome_evento": "Eros Ramazzotti World Tour",
       "id_artisti": ["A5"],   
       "data": {"$date": "2024-08-15T00:00:00.000Z"},
       "id_location": "L14",
       "biglietti": {
            "disponibili": 5000,
            "prezzo": 40,
            "id_ultimo_biglietto": 0
       }
    }
La collezione locations è composta da oggetti del tipo:
{ 
    "_id": "L1",
    "location_name": "Fabrique",
    "citta": "Milano",
    "stato": "Italia",
    "geolocation": {
        "type": "Point", 
        "coordinates": [9.252403, 45.447062]
    }
}

Abbiamo poi creato 40 eventi ed artisti e 20 locations, e distribuito gli artisti negli eventi. Abbiamo deciso di creare l'id per MongoDB per semplificare la ricerca in ogni collezione. Ipoteticamente sarebbe possibile aggiornare ogni JSON sia da MongoDB o aggiornando il JSON con altri valori. 
La fase successiva del progetto è stata il test direttamente su MongoDB per definire le query da tradurre per python e pymongo. Infine abbiamo creato le varie funzioni di menu in python e implementato le query MongoDB con pymongo per poter richiedere le informazioni necessarie al database.


--- funzionalità non implementate
I JSON non vengono caricati con Python, ma è necessario caricarli sul database MongoDB collegato o effettuare degli update da Python con pymongo. 
Una volta effettuata le ricerca, l'utente deve comprare necessariamente un biglietto. 
Nella ricerca per distanza l'utente non può modificare il raggio di ricerca, se non modificando il codice.
Non esiste un login per poter visionare i biglietti comprati, o i biglietti stampati all'utente.


--- modificare il server di connessione
Di default, l'utente si collega al server creato da noi. Risulta possibile modificare il database, inserendone uno personale, modificando le stringhe di connessione. Per farlo bisogna modificare il codice: aprire il file_lavoro.py e cambiare la stringa del cliente e il nome del server (default: 'biglietti').

N.B. In caso l'utente chiami le collezioni in MongoDB in maniera differente (default: 'artisti', 'eventi', 'locations') dovrà modificare anche i nomi dei database in ogni sezione di codice. 

--- bug conosciuti
VVV














