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
- VetService: http://localhost:8003/vets
- ConsultationService: http://localhost:8001/consultations
- FeedbackService: http://localhost:8002/feedbacks

## Endpoints:
- /vets
- /consultations
- /feedbacks
