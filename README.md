# QA Microservice Integration 
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/nadreal/qa-microservice-integration/ci-cd-pipeline.yml?branch=main&style=flat-square) &nbsp;&nbsp;
![Pytest](https://img.shields.io/badge/Pytest-tested-success?style=flat-square) &nbsp;&nbsp;
![Python Version](https://img.shields.io/badge/Python-3.11-blue?style=flat-square) &nbsp;&nbsp;
![Playwright](https://img.shields.io/badge/Playwright-automation-blueviolet?style=flat-square) &nbsp;&nbsp;
[![Allure Test Report](https://img.shields.io/badge/%20Report-Allure-purple)](https://nadreal.github.io/qa-microservice-integration/)

## Project Overview
 The project is a **FastAPI + PostgreSQL** backend microservice for **CRUD** operations. Designed with a modular and async-first architecture, it demonstrates best practices for building and testing microservices:

- Modular architecture: clear separation of api, services, db, and models
- Async database operations: powered by SQLAlchemy with async sessions and asyncpg
- Testing-ready: service abstraction for deterministic, isolated tests
- Docker-readyt: docker-compose setup for easy development

## Tech Stack
 - Backend: FastAPI (async)
 - ORM: SQLAlchemy 2.x (async ORM)
 - Database: PosgreSQL,asyncpg
 - Server: Uvicorn
 - Validation: Pydantic
 - Upcoming: Alembic migrations, Load testing (Locust), Kubernetes deplyment

## Project Structure 
```
├── workflows/
│   └── ci-cd-pipeline.yml   # CI/CD workflow
├── app/
│    │
│    ├── api\v1/
│    ├── ├── endpoints/
│    │   │   ├── health.py
│    │   │   └── item.py
│    │   ├── router.py
│    ├── auth/
│    ├── db/
│    │   └── base.py
│    │   └── config.py
│    │   └── initialise.py
│    │   └── session.py
│    ├── models/
│    ├── schemas/ 
│    ├── service/
│    └── main.py
├── tests/
├── docker-compose.yml
├── README.md
```
## Architecture Overview

- Service abstraction: business logic lives in service classes (e.g., ItemService) separate from API endpoints.
- Async-first design: all DB calls are asynchronous, improving scalability.
- Test isolation: services can be swapped with in-memory implementations for fast unit tests without touching the database.

## CI-CD Integration Overview
 - A GitHub Actions workflow is included to automatically run tests on each commit
 - Workflow file: .github/workflows/ci-cd-pipeline.yml
 - Triggered on: push and pull_request events

## API endpoints

- **GET `/health`** – API health check. Returns: {"status": "ok"}

- **GET `/users/{id}`** – Get a user by ID. Returns user JSON

- **POST `/users/`** – Create a new user. Send JSON: 

- **UPDATE `/user/{id}`** - Update existing user. 

- **DELETE `/users/{id}`** - Delete a user by ID.

## Test Reporting

<!-- - Open Allure [Test Report ](https://nadreal.github.io/qa-microservice-integration)  -->

## Author

👨‍🚀 Stevan Grubac [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourusername) <br>
💻 Software Engineer | QA Automation | DevOps

