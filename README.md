# Question-Answering Bot API

## Introduction

This project is a backend service built with FastAPI for handling data download and ingestion into Elasticsearch. It provides two primary endpoints for downloading and ingesting data.

## Project Description

The backend service offers the following functionalities:

- Download and Ingest Data: Downloads all ABN files, transforms them, and ingests the data into Elasticsearch.
- Ingest One File: Ingests a single file from the local directory into Elasticsearch.

## Technical Details

- Python: 3.12
- Pipenv: Used for managing Python packages and dependencies.
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- Elasticsearch: A search engine based on the Lucene library, used for indexing and searching the ingested data.

## Endpoints

`/download-and-ingest`
Downloads all ABN files, transforms them, and ingests the data into Elasticsearch.

`/ingest-one`
Ingests a single file from the local directory into Elasticsearch.

## Steps to Run, Test, and Deploy

### Prerequisites

- Python 3.9 or higher installed
- Docker installed (optional, for containerization)

1. Clone the Repository

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install Dependencies

   ```bash
   pip install pipenv
   pipenv install --dev
   ```

3. Set Environment Variables

Create a `.env.dev` file for development environment and `.env.prod` file for production environment.

4. Run the Application Locally

   ```bash
   make docker-compose-up
   ```

5. Test the API

The API can be tested at `http://localhost:8000/docs` when running the application locally.

6. API Documentation

The API documentation can be accessed at `http://localhost:8000/docs` when running the application locally. It provides detailed information about the available endpoints, request parameters, and response formats.
"""
