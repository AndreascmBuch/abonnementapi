import os 
import sqlite3

# Opret forbindelse til databasen
conn = sqlite3.connect("abonnement.db")
cursor = conn.cursor()

# Opret tabellen med abonnementsdata
cursor.execute('''
CREATE TABLE IF NOT EXISTS abonnement(
    subscription_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    kunde_id INTEGER,
    car_id INTEGER,
    term INTEGER,
    price_per_month REAL,
    start_month TEXT,
    end_month TEXT,
    restance BOOLEAN,
    contract_information TEXT )
''')


conn.commit()
conn.close()