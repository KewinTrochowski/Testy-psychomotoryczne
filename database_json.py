import json
import os
import datetime

session = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")

def save_results(results,game):
    if not os.path.exists(f"results/{session}"):
        os.mkdir(f"results/{session}")
    path = f"results/{session}/results.json"

    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, 'r') as plik:
            dane = json.load(plik)
    else:
        dane = {}
    try:
        dane[game].append(results)
    except:
        dane[game] = [results]

    # Zapisanie zaktualizowanych danych z nowym stringiem do pliku JSON
    with open(path, 'w') as plik:
        json.dump(dane, plik)

def read_results():
    if os.path.exists(f"results/{session}/results.json") and os.path.getsize(f"results/{session}/results.json") > 0:
        with open(f"results/{session}/results.json", 'r') as plik:
            dane = json.load(plik)
        return dane
    else:
        return {}

