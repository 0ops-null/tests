# Homework #15 — Testing Microservices

## Architecture

The project consists of two microservices:

1. Gateway Service
2. Todo Service

Gateway Service provides an HTTP API for clients and communicates
with Todo Service over HTTP.

Todo Service is responsible for storing Todo objects in SQLite.

## Unit tests

Unit tests were implemented for both microservices.

Todo Service tests cover:

- health check
- todo creation
- todo retrieval
- todo update
- todo deletion
- missing todo
- validation errors

Gateway Service tests use mocked HTTP requests and verify:

- health check
- GET /todos
- POST /todos
- communication with Todo Service

## Contract testing

A JSON Schema contract was created for Todo Service responses.

The contract defines:

- id as integer
- text as string
- complete as boolean

The contract test validates an actual Todo Service response
against the JSON Schema.

## Running tests

```bash
pip install -r requirements.txt
pytest -v
