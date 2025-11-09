# HMS Prescription Service

A microservice for managing medical prescriptions in a Hospital Management System (HMS), built with FastAPI and MySQL.

## Features

- ✅ Create and read prescriptions
- ✅ Prescription validation (no prescription without appointment)
- ✅ RESTful API with FastAPI
- ✅ MySQL database with SQLAlchemy ORM
- ✅ Docker containerization
- ✅ Docker Compose for multi-container setup
- ✅ Automatic database schema creation on startup
- ✅ CSV data seeding on initialization
- ✅ Modular project structure

## Database Schema

### Prescriptions Table

| Column           | Type         | Description                          |
|------------------|--------------|--------------------------------------|
| prescription_id  | INTEGER      | Primary key                          |
| appointment_id   | VARCHAR(50)  | Foreign key to appointment (required)|
| patient_id       | INTEGER      | Patient identifier                   |
| doctor_id        | INTEGER      | Doctor identifier                    |
| medication       | VARCHAR(255) | Medication name                      |
| dosage           | VARCHAR(50)  | Dosage format (e.g., 0-1-1)         |
| days             | INTEGER      | Number of days                       |
| issued_at        | DATETIME     | Timestamp of prescription issuance   |

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

**OR** for local development:

- Python 3.11+
- MySQL 8.0+

## Quick Start with Docker

### 1. Clone the repository

```bash
cd hms-prescription
```

### 2. Build and run with Docker Compose

```bash
docker compose up --build
```

This will:
- Build the FastAPI application Docker image
- Start MySQL database container
- Create database schema automatically
- Load initial data from `seed_data/hms_prescriptions.csv`
- Start the API service on `http://localhost:8000`

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4. Stop the services

```bash
docker-compose down
```

To remove volumes (database data):

```bash
docker-compose down -v
```

## API Endpoints

### Health Check

- `GET /` - Root endpoint with service info
- `GET /health` - Health check endpoint

### Prescription Endpoints

All prescription endpoints are prefixed with `/api/v1/prescriptions`

#### Create Prescription

```http
POST /api/v1/prescriptions/
Content-Type: application/json

{
  "appointment_id": "APPT-001",
  "patient_id": 101,
  "doctor_id": 5,
  "medication": "Amoxicillin",
  "dosage": "1-0-1",
  "days": 7
}
```

#### Get Prescription by ID

```http
GET /api/v1/prescriptions/{prescription_id}
```

#### Get All Prescriptions (with filters)

```http
GET /api/v1/prescriptions/?skip=0&limit=100&patient_id=101
```

Query Parameters:
- `skip` - Number of records to skip (default: 0)
- `limit` - Maximum records to return (default: 100, max: 500)
- `patient_id` - Filter by patient ID (optional)
- `doctor_id` - Filter by doctor ID (optional)
- `appointment_id` - Filter by appointment ID (optional)

#### Get Prescriptions by Patient

```http
GET /api/v1/prescriptions/patient/{patient_id}?skip=0&limit=100
```

#### Get Prescriptions by Doctor

```http
GET /api/v1/prescriptions/doctor/{doctor_id}?skip=0&limit=100
```

#### Get Prescriptions by Appointment

```http
GET /api/v1/prescriptions/appointment/{appointment_id}/prescriptions
```

## Local Development

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your local MySQL credentials
```

### 4. Ensure MySQL is running

```bash
# Start MySQL service
# Create database: prescription_db
```

### 5. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

| Variable     | Description                | Default            |
|--------------|----------------------------|--------------------|
| DB_HOST      | Database host              | mysql              |
| DB_PORT      | Database port              | 3306               |
| DB_USER      | Database username          | prescription_user  |
| DB_PASSWORD  | Database password          | prescription_pass  |
| DB_NAME      | Database name              | prescription_db    |
| APP_NAME     | Application name           | Prescription Service |
| APP_VERSION  | Application version        | 1.0.0              |
| DEBUG        | Debug mode                 | false              |



## Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **MySQL** - Relational database
- **Docker** - Containerization
- **Uvicorn** - ASGI server
- **PyMySQL** - MySQL driver for Python

## License

This project is part of the Hospital Management System (HMS) scalable assignment.

## Author

HMS Development Team

