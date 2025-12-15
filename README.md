# Event Management System (Django + DRF)

Event Management API implementing JWT auth, custom permissions, RSVPs, and reviews. Built for internship assignment.

## Features
- JWT authentication using `djangorestframework-simplejwt`.
- Event CRUD with organizer-only edits/deletes.
- Private event visibility restricted to invitees.
- RSVPs (Going/Maybe/Not Going) per event.
- Reviews with rating validation.
- Pagination, search, and filtering.
- Celery task stub for async email notifications (Redis broker).

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt  # if present, else install deps from settings
python manage.py migrate
python manage.py runserver
```

### Obtain JWT
1. Create a user (via `createsuperuser` or admin).
2. `POST /api/auth/token/` with `username` and `password`.
3. Use `Authorization: Bearer <access>` for subsequent requests.

## API Highlights
- `POST /api/events/` (auth): create event.
- `GET /api/events/`: list public events (+ private ones you organize/are invited to).
- `GET /api/events/{id}/`: event detail (private visibility enforced).
- `PUT/PATCH/DELETE /api/events/{id}/`: organizer only.
- `POST /api/events/{event_id}/rsvp/`: RSVP to event (invite required for private).
- `PATCH /api/events/{event_id}/rsvp/{rsvp_id}/`: update RSVP (self or staff).
- `POST /api/events/{event_id}/reviews/`: add review (invite required for private).
- `GET /api/events/{event_id}/reviews/`: list reviews.

Filtering/search: `?search=music&location=NYC&ordering=start_time`.

## Celery (optional bonus)
Start Redis locally, then run:
```bash
celery -A core worker --loglevel=info
```
Task example:
```python
from events.tasks import send_event_notification
send_event_notification.delay("Hello", "Body", "test@example.com")
```

## Running tests
```bash
.venv\Scripts\activate
python manage.py test
```

## Notes
- Email backend is console for local dev.
- Uses SQLite by default; swap `DATABASES` in `core/settings.py` for production.

