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
     
    Benvenuta/o !!       
 ______________________________________________
|TROVA I TUOI CONCERTI PREFERITI               |
|   a: Cerca per Artista                       |
|   d: Cerca per Date                          |
|   v: Cerca per Vicinanza                     |
|______________________________________________|""")

        scelta = input("\n> Inserisci la tua scelta (a, d, v): ").lower()
        
        match scelta:
            
            case "a":
                print('A')
                break
            case "d":
                print('D')
                break
            case "v":
                print('V')
                break
            case _:
                print("\n<<< Scelta non valida! Riprovare...")

def main():
    menu()
    
if __name__ == "__main__":
    main()
    
def cerca_artista(nome_ricerca):
    artisti_cercati = db['artisti']
    documenti_trovati = artisti_cercati.find(
        {'artista': nome_ricerca},
        {'_id': 0, 'artista.nome_arte': 1, 'lista_eventi': 1}
    )
    valori = [d for d in documenti_trovati]

    return valori
    
def cerca_per_vicinanza(lat, lon, distanza=7):
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
    venues = [d for d in locations_trovate]

    return venues
