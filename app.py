import sqlite3
from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os


# Database path, ensure it’s set properly for the environment


# Opret forbindelse til databasen
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

app = Flask(__name__)
load_dotenv() 
DB_PATH = os.getenv('DB_PATH', 'abonnement.db')

@app.route('/abonnement', methods=['POST'])
def create_abonnement():
    try:
        data = request.json
        
        required_fields = ["kunde_id", "car_id", "term", "price_per_month", "start_month", "end_month", "restance", "contract_information"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Feltet '{field}' mangler"}), 400

        kunde_id = data["kunde_id"]
        car_id = data["car_id"]
        term = data["term"]
        price_per_month = data["price_per_month"]
        start_month = data["start_month"]
        end_month = data["end_month"]
        restance = data["restance"]
        contract_information = data["contract_information"]

        # Check customer via microservice
        kunde_response = requests.get(f"https://kunde-api-dnecdehugrhmbghu.northeurope-01.azurewebsites.net/customers/{kunde_id}")
        if kunde_response.status_code != 200:
            return jsonify({"error": "Kunde ikke fundet"}), 404

        # Check car via microservice
        damage_response = requests.get(f"https://bildatabasedemo-hzfbegh6eqfraqdd.northeurope-01.azurewebsites.net/cars/{car_id}")
        if damage_response.status_code != 200:
            return jsonify({"error": "Skadesdata ikke fundet for bilen"}), 404

        # Insert data into the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO abonnement (kunde_id, car_id, term, price_per_month, start_month, end_month, restance, contract_information)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (kunde_id, car_id, term, price_per_month, start_month, end_month, restance, contract_information))
        conn.commit()
        conn.close()

        return jsonify({"message": "Abonnement oprettet succesfuldt"}), 201

    except Exception as e:
        return jsonify({"error": f"Der opstod en fejl: {str(e)}"}), 500

@app.route('/abonnement', methods=['GET'])
def get_abonnementer():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM abonnement ")
        subscription = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(subscription), 200
    except Exception as e:
        return jsonify({"error": "Der opstod en fejl"}), 500

@app.route('/abonnement/<int:subscription_id>', methods=['GET'])
def get_abonnement(subscription_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM abonnement WHERE subscription_id = ?", (subscription_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            subscription = dict(row)
            return jsonify(subscription), 200
        else:
            return jsonify({"error": "Abonnement ikke fundet"}), 404
    except Exception as e:
        return jsonify({"error": f"Serverfejl: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Abonnement",
        "version": "1.0.0",
        "description": "A RESTful API for managing abonnement"
    })

if __name__ == '__main__':
    app.run(debug=True)