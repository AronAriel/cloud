# Veterinary Services API

## Services:
- ConsultationService
- VetService
- FeedbackService

## How to run:

uvicorn main:app --reload --port 8000

## Run all services with Docker:

```bash
docker compose up --build
```

Service URLs:
- VetService GraphQL: http://localhost:8003/graphql
- ConsultationService: http://localhost:8001/consultations
- FeedbackService: http://localhost:8002/feedbacks

## Endpoints:
- /graphql (VetService query: `{ vets { id name specialization } }`)
- /consultations
- /feedbacks
