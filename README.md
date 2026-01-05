# RPG Character Profile Management System
![Status: Work in Progress](https://img.shields.io/badge/status-work--in--progress-orange)
## Project Overview
This project is a technical exercise focused on building a character management system using **FastAPI**, **PostgreSQL**, and **Docker**. The application allows users to create, store, and edit character profiles with persistent storage. It features a modern modular backend architecture and secure authentication.
## Technical Features
* **FastAPI Backend**: Organized using `APIRouter` for modularity across authentication, user management, and character operations.
* **JWT Authentication**: Implements `OAuth2PasswordBearer` and `pyjwt` for stateless session management.
* **PostgreSQL Database**: Stores users, character data, and character generation seeds. It uses `psycopg` with connection pooling for efficient database access. Supports full Create, Read, Update, and Delete operations. 
* **Pydantic Validation**: Uses schemas to enforce data types and validate API requests/responses.

## Local Setup (Docker)

The application is fully containerized using Docker Compose.

1.  **Environment Setup**:
    Copy the example environment file and configure your variables:
    ```bash
    cp .env_example .env
    ```
    Ensure you define the `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `JWT_SECRET_KEY`.

2.  **Run Application**:
    Build and start the services:
    ```bash
    docker-compose up --build
    ```
    This command starts the database, backend (FastAPI), and frontend (Streamlit) containers.

## Access Information

* **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Frontend Dashboard**: [http://localhost:8501](http://localhost:8501)
* **Database**: Port `5432`

## Roadmap
- [x] Functional FastAPI Backend & PostgreSQL Integration
- [x] Secure JWT Authentication System
- [x] Procedural Character Generation Service
- [x] Fully Dockerized Deployment
- [ ] **In Progress:** Streamlit Dashboard for Data Visualization and CRUD Testing.
- [ ] **Planned:** Frontend transition to **Next.js & TypeScript**.
- [ ] **Planned:** Automated CI/CD pipelines via GitHub Actions.

## Project Structure
```text
.
├── backend
│   ├── app
│   │   ├── routers           # API endpoint definitions (Auth, User, Character)
│   │   │   ├── auth.py
│   │   │   ├── character.py
│   │   │   └── user.py
│   │   ├── crud.py           # Database CRUD logic
│   │   ├── database.py       # PostgreSQL connection pool management
│   │   ├── db_init.py        # Database initialization and data seeding
│   │   ├── main.py           # FastAPI application entry point
│   │   ├── schemas.py        # Pydantic models for data validation
│   │   └── security.py       # JWT and password hashing implementation
│   ├── service
│   │   └── character_generator.py # Procedural character generation logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── Dockerfile
│   ├── frontend_main.py      # Streamlit dashboard interface (Under Development)
│   └── requirements.txt
├── docker-compose.yml        # Multi-container orchestration
├── .env_example              # Environment variable template
└── README.md
