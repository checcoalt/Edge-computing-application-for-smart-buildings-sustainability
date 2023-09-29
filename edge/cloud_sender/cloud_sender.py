# import mqttx.py
from ..mqttx.mqttx import *
from  edge.config import *
import requests
import json

mqtt_client = Client(BROKER_IP_ADDRESS, TOPIC_MEASUREMENTS)
# Convertire i dati JSON in una stringa
json_data = json.dumps(data_to_send)

# Definire l'URL di destinazione
url = "http://127.0.0.1/display_json"  # Sostituisci con l'URL effettivo

# Impostare le intestazioni HTTP (opzionale)
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YourAccessToken"  # Aggiungi l'autorizzazione se necessario
}

# Effettuare la richiesta HTTP POST con i dati JSON nel corpo
response = requests.post(url, data=json_data, headers=headers)

# Verificare la risposta
if response.status_code == 200:
    print("Richiesta inviata con successo.")
else:
    print("Errore nella richiesta:", response.status_code)
    print(response.text)  # Puoi stampare la risposta per ottenere ulteriori dettagli sull'errore, se presente