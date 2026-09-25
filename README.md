# MY README 
# Event Management API

A simple RESTful API built with Flask that manages events in memory (no database).
It supports full CRUD-style operations: listing events, creating an event, updating
an event's title, and deleting an event.

## Running it

```bash
python --version
pip install flask
python app.py
```

The server runs at `http://localhost:5000`.

## Routes

### `GET /`
Welcome message, confirms the API is running.

**Response `200`**
```json
{ "message": "Welcome to the Event Management API" }
```

---

### `GET /events`
Returns every event currently stored.

**Response `200`**
```json
[
  { "id": 1, "title": "Tech Meetup" },
  { "id": 2, "title": "Python Workshop" }
]
```

---

### `POST /events`
Creates a new event. Requires a JSON body with a non-empty `title`.

**Request**
```json
{ "title": "Hackathon" }
```

**Response `201`**
```json
{ "id": 3, "title": "Hackathon" }
```

**Response `400`** (missing/empty `title`)
```json
{ "error": "A non-empty 'title' field is required" }
```

---

### `PATCH /events/<id>`
Updates the `title` of the event with the given id.

**Request**
```json
{ "title": "Hackathon 2025" }
```

**Response `200`**
```json
{ "id": 1, "title": "Hackathon 2025" }
```

**Response `404`** (no event with that id)
```json
{ "error": "Event with id 999 not found" }
```

**Response `400`** (missing/empty `title`)
```json
{ "error": "A non-empty 'title' field is required" }
```

---

### `DELETE /events/<id>`
Removes the event with the given id.

**Response `200`**
```json
{ "message": "Event 2 deleted successfully" }
```

**Response `404`** (no event with that id)
```json
{ "error": "Event with id 999 not found" }
```

## Design notes

- Data is stored in an in-memory list of `Event` objects (no database).
- `find_event(event_id)` is a shared helper used by `PATCH` and `DELETE` to avoid
  repeating the same lookup/404 logic.
- New events get an auto-incrementing id from a `next_id` counter, so ids stay
  unique even after deletions.
- All responses are JSON via `jsonify()`, with status codes following REST
  conventions (`201` for create, `200` for successful read/update/delete,
  `400` for bad input, `404` for missing resources).