#file di lavoro

from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

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
                    nome_artista, lista_eventi = menu_artisti(a_valori)
                    print(f'Eventi disponibili per {nome_artista}')
                    id_evento = menu_scelta_evento(lista_eventi, db)
                    biglietto = acquista_biglietti(id_evento, db)
                    break
            case "d":
                print('RICERCA PER DATA\n')
                while True:
                    print('Inserisci il periodo che vuoi cercare in formato anno-mese-giorno\n')
                    d_inizio_ricerca = str(input('Data inizio: ')) 
                    d_fine_ricerca =  str(input('Data fine: '))
                    d_valori = cerca_data(d_inizio_ricerca, d_fine_ricerca, db)
                    id_evento = menu_date(d_valori)
                    biglietto = acquista_biglietti(id_evento, db)
                    break
            case "v":
                print('RICERCA PER VICINANZA (7 km)\n')
                while True:
                    latitudine = float(input('Scrivi la latitudine: '))
                    longitudine = float(input('Scrivi la longitudine: '))
                    v_ricerca = cerca_per_vicinanza(latitudine, longitudine, db)
                    #print(v_ricerca)
                    lista_eventi = menu_distanze(v_ricerca, db)
                    id_evento = menu_scelta_evento(lista_eventi, db)
                    biglietto = acquista_biglietti(id_evento, db)
                    break
            case "e":
                print('RICERCA PER EVENTI\n')
                while True:
                    e_ricerca = '^' + str(input('Inserisci il nome dell\'evento da cercare: ')).lower()
                    e_valori = cerca_evento(e_ricerca, db)
                    nome_evento = menu_evento(e_valori)
                    id_evento = menu_scelta_evento(nome_evento, db)
                    biglietto = acquista_biglietti(id_evento, db)
                    break
                    #else:
                        #print("Nessun evento trovato. Riprova.")
            case "x":
                print("Chiusura applicazione...")
                break
            case _:
                print("\n<<< Scelta non valida! Riprovare...")

    
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
        {'_id': 0, 'id_artisti': 0, 'data': 1, 'id_location': 0, 'biglietti.disponibili': 1, 'biglietti.prezzo': 1} 
    )
    return list(e_documenti_trovati)

def menu_evento(e_documenti_trovati):
    num_eventi = len(e_documenti_trovati)
    diz = {}
    for i in range(num_eventi):
        print(f'{i+1} |', e_documenti_trovati[i]['nome_evento'])
        diz.update({i+1: e_documenti_trovati[i]['nome_evento']})
    while True:
        print('Quale evento stai cercando?\n')
        scelta_utente = int(input(('Evento n: ')))
        nome_evento = diz.get(scelta_utente, False)
        if nome_evento:
            break
    return nome_evento


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
        {'id_location': id_luogo}
    )
    return list(l_documenti_trovati)

### RICERCA PER DATA

'''
def cerca_data(db):
    print('Inserisci il periodo che vuoi cercare in formato anno-mese-giorno\n')
    data_inizio = str(input('Data inzio: '))
    data_fine = str(input('Data fine: ')) 
    data_inizio_dt = dt.datetime.strptime(data_inizio, '%Y-%m-%dT%H:%M:%S.000+00:00')
    data_fine_dt = dt.datetime.strptime(data_fine, '%Y-%m-%dT%H:%M:%S.000+00:00')
    results = eventi_cercati.find({'nome_evento': 1, 'data': 1},
    {'released': {
        '$gte': data_inizio_dt,
        '$lte': data_fine_dt
    }})
    eventi = [r for r in results]
    return eventi
'''
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
    return id_evento


def acquista_biglietti(id, db):
    db_eventi = db['eventi']
    evento = db_eventi.find({
        '_id': id
    },
    {'nome_evento': 1,'biglietti.disponibili': 1, 'biglietti.prezzo': 1, 'biglietti.id_ultimo_biglietto': 1})
    info_biglietti = list(evento)
    while True:
        num_biglietti = int(input("Quanti biglietti vuoi acquistare? "))
        if num_biglietti <= 0 or num_biglietti > info_biglietti[0]['biglietti']['disponibili']:
            print("Non puoi acquistare così tanti biglietti!")
        else:
            print(f'Ecco i tuoi biglietti per un totale di {info_biglietti[0]["biglietti"]["prezzo"]*num_biglietti:.2f} € :\n')
            for i in range(num_biglietti):
                db_eventi.update_one(
                    {'_id': id},
                    {'$inc': {'biglietti.id_ultimo_biglietto': 1}}
                    )
                print(f'{info_biglietti[0]["nome_evento"]}, biglietto n. B{info_biglietti[0]["biglietti"]["id_ultimo_biglietto"]}')

                # Aggiorna la disponibilità dei biglietti
    
            db_eventi.update_one(
                    {'_id': id},
                    {'$inc': {'biglietti.id_ultimo_biglietto': -num_biglietti}}
            )

            print(f"Disponibilità aggiornata\n{info_biglietti[0]['nome_evento']} - disponibili: {info_biglietti[0]['biglietti']['disponibili']}")
            return True


if __name__ == "__main__":
    main()