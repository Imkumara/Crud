from flask import Flask, jsonify, request

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Simulated data
# ---------------------------------------------------------------------------
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Tracks the next id to assign so new events always get a unique id,
# even after other events have been deleted.
next_id = 3


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def find_event(event_id):
    """Return the Event with the given id, or None if it doesn't exist."""
    for event in events:
        if event.id == event_id:
            return event
    return None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Event Management API"})


@app.route("/events", methods=["GET"])
def get_events():
    # Return every event as a JSON array
    return jsonify([event.to_dict() for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    global next_id

    data = request.get_json(silent=True)

    # Validate the request body
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "A non-empty 'title' field is required"}), 400

    new_event = Event(next_id, data["title"])
    events.append(new_event)
    next_id += 1

    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    data = request.get_json(silent=True)
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "A non-empty 'title' field is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    events.remove(event)
    return jsonify({"message": f"Event {event_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)