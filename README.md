# QA Microservice Integration 
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/nadreal/qa-microservice-integration/ci-cd-pipeline.yml?branch=main&style=flat-square) &nbsp;&nbsp;
![Pytest](https://img.shields.io/badge/Pytest-tested-success?style=flat-square) &nbsp;&nbsp;
![Python Version](https://img.shields.io/badge/Python-3.11-blue?style=flat-square) &nbsp;&nbsp;
![Playwright](https://img.shields.io/badge/Playwright-automation-blueviolet?style=flat-square) &nbsp;&nbsp;
[![Allure Test Report](https://img.shields.io/badge/%20Report-Allure-purple)](https://nadreal.github.io/qa-microservice-integration/)

## Project Overview
 The project is a production style **FastAPI + PostgreSQL** microservice implementing full **CRUD** operations. Designed with a modular, async-first architecture, it demonstrates backend engineering best practices for building and validating microservices:

- Layered architecture (API → Service → ORM → Database)
- Explicit transaction handling and rollback management
- Proper HTTP status mapping (e.g. 409 Conflict for unique constraint violations)
- Integration testing against a real PostgreSQL database
- Automated CI validation with GitHub Actions and Allure reporting
- Docker-based development environment

## Tech Stack
 - Backend: FastAPI (async)
 - ORM: SQLAlchemy 2.x (async ORM)
 - Database: PostgreSQL (asyncpg driver)
 - Server: Uvicorn
 - Validation: Pydantic
 - CI/CD: GitHub Actions
 - Test reporting (Allure)

 **Planned extensions:**
 - Alembic migrations
 - Load testing (Locust)
 - Container orchestration (Kubernetes)

 
## Project Structure 
```
├── .github/workflows/
│   └── ci-cd-pipeline.yml   # CI/CD workflow
├── app/
│    ├── api\v1/
│    ├── ├── endpoints/
│    │   │   ├── health.py
│    │   │   ├── root.py
│    │   │   └── item.py
│    │   ├── router.py
│    ├── auth/
│    ├── db/
│    │   └── base.py
│    │   └── config.py
│    │   └── initialise.py
│    │   └── session.py
│    ├── models/
│    │   └── item.py
│    ├── schemas/ 
│    │   └── item.py
│    ├── services/
│    │   └── item_service.py
│    └── main.py
├── tests/
│    ├── api/ 
│    ├── integration/
│    │   └── test_api_items_update_list.py
│    │   └── test_api_items.py
│    └── unit/
├── docker-compose.yml
├── README.md
```
## Architecture Overview

- **Service abstraction:** Business logic resides in dedicated service classes (e.g., `ItemService`), keeping API endpoints thin and testable.
- **Async-first design:** All database operations use async SQLAlchemy sessions to support scalable I/O handling.
- **Transaction safety:** Explicit commit/rollback handling ensures session integrity after constraint violations.
- **Test isolation:** Integration tests validate full request lifecycle; service layer enables isolated unit testing when needed.

## CI-CD Integration with GitHub Actions workflow

- Starts PostgreSQL service container
- Installs dependencies
- Runs pytest
- Publishes Allure report

Triggered on:
- push
- pull_request

## API endpoints

- GET `/api/v1/health`
- GET `/api/v1/items/`
- GET `/api/v1/items/{id}`
- POST `/api/v1/items/`
- PUT `/api/v1/items/{id}`
- DELETE `/api/v1/items/{id}`

## Test Reporting

- [ Allure Test Report ](https://nadreal.github.io/qa-microservice-integration/index.html) 
- [ Coverage Report ](htmlcov/index.html)

## Author

👨‍🚀 Stevan Grubac [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourusername) <br>
💻 Software Engineer | QA Automation | DevOps

