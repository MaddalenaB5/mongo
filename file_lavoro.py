#file di lavoro

from pymongo import MongoClient
from datetime import datetime
from time import sleep

client = MongoClient('mongodb+srv://maddalenabozzola_:1iEoHJKaFeMqZDHH@ufs13.p4dqcok.mongodb.net/?retryWrites=true&w=majority&appName=UFS13')

db = client['biglietti']
#print(db)

def main():
    menu(db)

def menu(db):
    while True:
        print(f"""
=================================================
     
    Benvenuta/o su TicketTwo!!       
 ______________________________________________
|TROVA I TUOI CONCERTI PREFERITI               |
|   a: Cerca per Artista                       |
|   d: Cerca per Date                          |
|   e: Cerca per Evento                        |
|   v: Cerca per Vicinanza                     |
|                                              |
|   x: Esci dall'Applicazione                  |
|______________________________________________|""")


        scelta = input("\n> Inserisci la tua scelta (a, d, e, v, x): ").lower()
        
        match scelta:
            case "a":
                print('RICERCA PER ARTISTA\n')
                while True:
                    a_ricerca = '^' + str(input('Inserisci il nome dell\'artista da cercare: ')).lower()
                    a_valori = cerca_artista(a_ricerca, db)
                    if a_valori:
                        nome_artista, lista_eventi = menu_artisti(a_valori)
                        print(f'Eventi disponibili per {nome_artista}')
                        id_evento = menu_scelta_evento(lista_eventi, db)
                        biglietto = acquista_biglietti(id_evento, db)
                    else:
                        print('Nessun risultato trovato! Torno al menù principale!')
                    sleep(3)
                    break
            case "d":
                print('RICERCA PER DATA\n')
                while True:
                    print('Inserisci il periodo che vuoi cercare in formato anno-mese-giorno\n')
                    d_inizio_ricerca = str(input('Data inizio: ')) 
                    d_fine_ricerca =  str(input('Data fine: '))
                    if d_inizio_ricerca > d_fine_ricerca:
                        print('Hai scritto le date al contrario! Risolvo io!')
                        d_inizio_ricerca, d_fine_ricerca = d_fine_ricerca, d_inizio_ricerca
                    d_valori = cerca_data(d_inizio_ricerca, d_fine_ricerca, db)
                    if d_valori:
                        id_evento = menu_date(d_valori)
                        biglietto = acquista_biglietti(id_evento, db)
                    else:
                        print('Nessun risultato trovato! Torno al menù principale!')
                    sleep(3)
                    break
            case "v":
                print('RICERCA PER VICINANZA (7 km)\n')
                while True:
                    latitudine = float(input('Scrivi la latitudine: '))
                    longitudine = float(input('Scrivi la longitudine: '))
                    v_ricerca = cerca_per_vicinanza(latitudine, longitudine, db)
                    if v_ricerca:
                        lista_eventi = menu_distanze(v_ricerca, db)
                        id_evento = menu_scelta_evento(lista_eventi, db)
                        biglietto = acquista_biglietti(id_evento, db)
                    else:
                        print('Nessun risultato trovato! Torno al menù principale!')
                    sleep(3)
                    break
            case "e":
                print('RICERCA PER EVENTI\n')
                while True:
                    e_ricerca = '^' + str(input('Inserisci il nome dell\'evento da cercare: ')).lower()
                    e_valori = cerca_evento(e_ricerca, db)
                    if e_valori:
                        id_evento = menu_evento(e_valori)
                        biglietto = acquista_biglietti(id_evento, db)
                    else:
                        print('Nessun risultato trovato! Torno al menù principale!')
                    sleep(3)
                    break
            case "x":
                print("Chiusura applicazione...")
                sleep(3)
                break
            case _:
                print("\n<<< Scelta non valida! Riprovare...")
                sleep(2)
    
def cerca_artista(a_ricerca, db):
    artisti_cercati = db['artisti']
    a_documenti_trovati = artisti_cercati.find(   #$regex permette di trovare la parola anche se è una sottostringa del nome completo dell'artista
        {'artista.nome_arte': {'$regex': a_ricerca, '$options': 'i'}},
        {'_id': 0, 'artista.nome_arte': 1, 'lista_eventi': 1}
    )
    return list(a_documenti_trovati)


def menu_artisti(lista_artisti):
    num_artisti = len(lista_artisti)
    diz = {}
    for i in range(num_artisti):
        print(f'{i+1} |', lista_artisti[i]['artista']['nome_arte'])
        diz.update({i+1: lista_artisti[i]['artista']['nome_arte']})
    while True:
        print('Quale artista stai cercando?\n')
        scelta_utente = int(input(('Artista n: ')))
        nome_artista = diz.get(scelta_utente, False)
        if nome_artista:
            break
    return nome_artista, lista_artisti[scelta_utente-1]['lista_eventi']
        

### RICERCA PER EVENTO


def cerca_evento(e_ricerca, db):
    eventi_cercati = db['eventi']
    e_documenti_trovati = eventi_cercati.find(
        {'nome_evento': {'$regex': e_ricerca, '$options': 'i'}},
        {'_id': 1, 'nome_evento': 1, 'data': 1, 'biglietti.disponibili': 1, 'biglietti.prezzo': 1} 
    )
    return list(e_documenti_trovati)

def menu_evento(e_documenti_trovati):
    num_eventi = len(e_documenti_trovati)
    diz = {}
    for i in range(num_eventi):
        print(f"{i+1} | {e_documenti_trovati[i]['nome_evento']} - data {e_documenti_trovati[i]['data'].strftime('%Y-%m-%d')}")
        diz.update({i+1: e_documenti_trovati[i]['_id']})
    while True:
        print('Quale evento stai cercando?\n')
        scelta_utente = int(input(('Evento n: ')))
        id_evento = diz.get(scelta_utente, False)
        if id_evento:
            break
    return id_evento


### RICERCA PER VICINANZA    # Milano - 45.45 | 9.2

def cerca_per_vicinanza(lat, lon, db, distanza=7):  
    raggio = distanza/6378.1 # conversione km to radianti
    locs = db['locations']
    coord = [lon, lat]
    locations_trovate = locs.find({
        "geolocation.coordinates": {
            "$geoWithin": {
                "$centerSphere": [coord, raggio]
            }
        }
    }, 
    {'_id': 1, 'location_name': 1, 'citta': 1})

    return list(locations_trovate)


def menu_distanze(locations_trovate, db):
    num_distanze = len(locations_trovate)
    diz = {}
    for i in range(num_distanze):
        print(f"{i+1} | {locations_trovate[i]['location_name']} a {locations_trovate[i]['citta']}")
        diz.update({i+1: locations_trovate[i]['_id']})
    while True:
        print('Quale luogo stai cercando?\n')
        scelta_utente = int(input(('Luogo n: ')))
        id_luogo = diz.get(scelta_utente, False)
        if id_luogo:
            break
    luoghi_cercati = db['eventi']
    l_documenti_trovati = luoghi_cercati.find(
        {'id_location': id_luogo},
        {'_id': 1}
    )
    lista_eventi_trovati = list(l_documenti_trovati)
    lista_id_eventi = [doc['_id'] for doc in lista_eventi_trovati]
    return lista_id_eventi 

### RICERCA PER DATA

def cerca_data(data_inizio, data_fine, db):
    date_cercate = db['eventi']
    d_documenti_trovati = date_cercate.find({
        'data': {
            '$gte': datetime.strptime(data_inizio, '%Y-%m-%d'),
            '$lte': datetime.strptime(data_fine, '%Y-%m-%d')
    }},
    {'_id': 1,'nome_evento': 1, 'data': 1})
    return list(d_documenti_trovati)

def menu_date(d_documenti_trovati):
    num_date = len(d_documenti_trovati)
    diz = {}
    for i in range(num_date):
        print(f'{i+1} |', d_documenti_trovati[i]['nome_evento'])
        diz.update({i+1: d_documenti_trovati[i]['nome_evento']})
    while True:
        print('Quale evento stai cercando?\n')
        scelta_utente = int(input(('Evento n: ')))
        id_evento = diz.get(scelta_utente, False)
        if id_evento:
            break
    return d_documenti_trovati[scelta_utente-1]['_id']


### ALTRE FUNZIONI

def menu_scelta_evento(lista_eventi, db):
    db_eventi = db['eventi']
    eventi_disponibili_trovati = db_eventi.find(
            {'_id': {'$in': lista_eventi}},
            {'_id': 1,'nome_evento': 1, 'data': 1, 'biglietti.disponibili': 1, 'biglietti.prezzo': 1}
        )
    eventi_disponibili = list(eventi_disponibili_trovati)
    num_eventi = len(eventi_disponibili)
    diz = {}
    for i in range(num_eventi):
        nome_evento = eventi_disponibili[i]["nome_evento"]
        data_evento = eventi_disponibili[i]["data"].strftime("%Y-%m-%d")
        biglietti_disp = eventi_disponibili[i]["biglietti"]["disponibili"]
        if biglietti_disp == 0:
            biglietti_disp = 'SOLD-OUT'
        prezzo_biglietto = eventi_disponibili[i]["biglietti"]["prezzo"]
        print(f'{i+1} | {nome_evento} - data: {data_evento} - disp: {biglietti_disp} - prezzo: {prezzo_biglietto}' )
        diz.update({i+1: eventi_disponibili[i]['_id']})
    while True:
        print('Quale evento stai cercando?\n')
        scelta_utente = int(input(('Evento n: ')))
        id_evento = diz.get(scelta_utente, False)
        if id_evento:
            break
        else:
            print('Inserire di nuovo il numero\n')
    return id_evento

def acquista_biglietti(id, db):
    db_eventi = db['eventi']
    evento = db_eventi.find({
        '_id': id
    },
    {'nome_evento': 1,'biglietti.disponibili': 1, 'biglietti.prezzo': 1, 'biglietti.id_ultimo_biglietto': 1})
    info_biglietti = list(evento)
    #print(info_biglietti)
    while True:
        biglietti_disponibili = info_biglietti[0]['biglietti']['disponibili']
        num_biglietti_comprati = int(input("Quanti biglietti vuoi acquistare? "))
        if num_biglietti_comprati <= 0 or num_biglietti_comprati > biglietti_disponibili:
            print("Non puoi acquistare così tanti biglietti!")
        else:
            totale = info_biglietti[0]["biglietti"]["prezzo"]*num_biglietti_comprati
            numero_ultimo_biglietto = info_biglietti[0]["biglietti"]["id_ultimo_biglietto"]
            id_biglietto_iniziale = numero_ultimo_biglietto
            print(f'Ecco i tuoi biglietti per un totale di {totale:.2f} € :\n')
            for i in range(num_biglietti_comprati):
                print(f'Stampa biglietto n. B{numero_ultimo_biglietto + 1} - evento: {info_biglietti[0]["nome_evento"]}')
                numero_ultimo_biglietto += 1
                sleep(2)

            db_eventi.update_one(
                    {'_id': id},
                    {'$set': {
                        'biglietti.id_ultimo_biglietto': 
                            id_biglietto_iniziale + num_biglietti_comprati
                    }}
                    )

                # Aggiorna la disponibilità dei biglietti
    
            db_eventi.update_one(
                {'_id': id},
                {'$set': {
                        'biglietti.disponibili': 
                            biglietti_disponibili - num_biglietti_comprati
                    }} 
                )
            
            evento_aggiornato = list(db_eventi.find({
            '_id': id
            },
            {'nome_evento': 1,'biglietti.disponibili': 1}))
            
            print(f"Disponibilità aggiornata\n{evento_aggiornato[0]['nome_evento']} - disponibili: {evento_aggiornato[0]['biglietti']['disponibili']}")
            break

if __name__ == "__main__":
    main()
