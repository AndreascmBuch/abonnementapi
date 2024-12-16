# Abonnement Microservice

Dette er en RESTful API til at håndtere abonnementsdata for biludlejningstjenester. Mikroservicen opretter og henter abonnementsoplysninger, herunder kundeoplysninger, bilid, abonnementsperiode og pris. Den bruger Flask og SQLite til at gemme abonnementsdata og Flask JWT Extended til at sikre endpoints.

## Funktioner
- Oprettelse af abonnement (POST)
- Hentning af alle abonnementer (GET)
- Hentning af specifikt abonnement via subscription_id (GET)
- JWT-baseret autentificering

## Teknologier
- Python 3.10
- Flask
- SQLite
- Flask JWT Extended
- Gunicorn (til produktion)

## Installation

Følg disse trin for at køre tjenesten lokalt:

### 1. Klon repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Opret et virtuelt miljø og installer afhængigheder
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Opsæt miljøvariabler
Opret en .env-fil i roden af projektet med følgende indhold:
```env
DB_PATH=abonnement.db
FLASK_ENV=development
KEY=din_jwt_nøgle
```

### 4. Start applikationen
For at starte Flask-applikationen i udviklingsmiljøet:
```bash
flask run
```
Applikationen vil være tilgængelig på http://127.0.0.1:5000/.

### 5. Start applikationen med Gunicorn (produktion)
For at køre applikationen i et produktionsmiljø, skal du bruge Gunicorn:
```bash
gunicorn --bind 0.0.0.0:80 app:app
```

## Endpoints

### GET /
Viser grundlæggende information om tjenesten:
```json
{
  "service": "Abonnement",
  "version": "1.0.0",
  "description": "A RESTful API for managing abonnement"
}
```

### GET /debug
Viser debugging information om miljøvariabler:
```json
{
  "JWT_SECRET_KEY": "din_jwt_nøgle",
  "Database_Path": "abonnement.db"
}
```

### POST /abonnement
Opretter et nyt abonnement. Kræver en JWT-token i anmodningshovedet (Authorization: Bearer <token>).
- **Request Body:**
  ```json
  {
    "kunde_id": 1,
    "car_id": 101,
    "term": 12,
    "price_per_month": 500,
    "start_month": "2024-01-01",
    "end_month": "2024-12-31",
    "restance": 0,
    "contract_information": "Standard contract"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Abonnement oprettet succesfuldt"
  }
  ```

### GET /abonnement
Henter alle abonnementer. Kræver en JWT-token i anmodningshovedet.
- **Response:**
  ```json
  [
    {
      "subscription_id": 1,
      "kunde_id": 1,
      "car_id": 101,
      "term": 12,
      "price_per_month": 500,
      "start_month": "2024-01-01",
      "end_month": "2024-12-31",
      "restance": 0,
      "contract_information": "Standard contract"
    }
  ]
  ```

### GET /abonnement/<int:subscription_id>
Henter et specifikt abonnement ved hjælp af subscription_id. Kræver en JWT-token i anmodningshovedet.
- **Response:**
  ```json
  {
    "subscription_id": 1,
    "kunde_id": 1,
    "car_id": 101,
    "term": 12,
    "price_per_month": 500,
    "start_month": "2024-01-01",
    "end_month": "2024-12-31",
    "restance": 0,
    "contract_information": "Standard contract"
  }
  ```

## Database

Applikationen bruger en SQLite-database til at gemme abonnementsdata. Tabellen `abonnement` indeholder følgende felter:

- `subscription_id` (INTEGER, Primærnøgle)
- `kunde_id` (INTEGER)
- `car_id` (INTEGER)
- `term` (INTEGER)
- `price_per_month` (REAL)
- `start_month` (TEXT)
- `end_month` (TEXT)
- `restance` (INTEGER)
- `contract_information` (TEXT)

## Autentificering

Alle beskyttede endpoints kræver en JWT-token, som skal sendes i headeren af anmodningen under navnet `Authorization` med præfikset `Bearer`.

For at få en JWT-token kan du bruge et af de eksisterende endpoints eller implementere en login-mekanisme, der genererer tokenet.

## Deployment

### Docker

For at bygge og køre applikationen i Docker, kan du bruge følgende kommandoer:
```bash
docker build -t abonnement-service .
docker run -p 80:80 abonnement-service
```

### Azure

For at implementere denne service på Azure, kan du oprette en App Service og deployere Docker-containeren. Sørg for at konfigurere miljøvariablerne i Azure App Service.

## Licens

Dette projekt er licenseret under MIT-licensen - se LICENSE for detaljer.
