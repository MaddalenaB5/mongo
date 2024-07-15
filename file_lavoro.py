#file di lavoro

from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://maddalenabozzola_:1iEoHJKaFeMqZDHH@ufs13.p4dqcok.mongodb.net/?retryWrites=true&w=majority&appName=UFS13')

db = client['biglietti']
#print(db)

def menu():
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


        scelta = input("\n> Inserisci la tua scelta (a, d, v): ").lower()
        
        match scelta:
            
            case "a":
                while True:
                    a_ricerca = str(input('Inserisci il nome dell\'artista da cercare: ')).lower()
                    a_valori = cerca_artista(a_ricerca)
                    if a_valori:
                        for a_valore in a_valori:
                            print(a_valore)
                        break
                    else:
                        print("Nessun evento trovato. Riprova.")
                break
            case "d":
                print('RICERCA PER DATA\n')
                while True:
                    d_inizio_ricerca = str(input('Data inizio: ')) 
                    d_fine_ricerca =  str(input('Data fine: '))
                    d_valori = cerca_data(d_inizio_ricerca, d_fine_ricerca, db)
                    #print(d_valori)
                    lista_eventi_date = menu_date(d_valori)
                    id_evento = menu_scelta_evento(lista_eventi_date, db)
                    biglietto = acquista_biglietti(id_evento, db)

                break
            case "v":
                print('RICERCA PER VICINANZA\nScrivi le coordinate da cui vuoi cercare le location più vicine (7 km)')
                latitudine = float(input('Scrivi la latitudine: '))
                longitudine = float(input('Scrivi la longitudine: '))
                ricerca_v = cerca_per_vicinanza(latitudine, longitudine)
                #mostra_risultati_ricerca(ricerca_v)
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

def main():
    menu()
    
if __name__ == "__main__":
    main()
    
def cerca_artista(a_ricerca):
    artisti_cercati = db['artisti']
    a_documenti_trovati = artisti_cercati.find(   #$regex permette di trovare la parola anche se è una sottostringa del nome completo dell'artista
        {'artista.nome_arte': {'$regex': a_ricerca}},
        {'_id': 0, 'artista.nome_arte': 1, 'lista_eventi': 1}
    )
    return list(a_documenti_trovati)

### RICERCA PER EVENTO


def cerca_evento(e_ricerca):
    eventi_cercati = db['eventi']
    e_documenti_trovati = eventi_cercati.find(
        {'nome_evento': {'$regex': e_ricerca}},
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
    })

    return list(locations_trovate)

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
    print('Inserisci il periodo che vuoi cercare in formato anno-mese-giorno\n')
    date_cercate = db['eventi']
    d_documenti_trovati = date_cercate.find({
        'data': {
            '$gte': datetime.strptime(data_inizio, '%Y-%m-%d'),
            '$lte': datetime.strptime(data_fine, '%Y-%m-%d')
    }},
    {'nome_evento': 1, 'data': 1})
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
        nome_evento = diz.get(scelta_utente, False)
        if nome_evento:
            break
    return nome_evento


### ALTRE FUNZIONI

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
