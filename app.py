from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
  def __init__(self, id, title):
    self.id = id
    self.title = title

  def to_dict(self):
    return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
  # Retrieve JSON data from the request
  data = request.get_json(silent=True) # reads JSON, invalid of missin JSON returns None
  
  # Check the title was provided
  if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not data["title"].strip():
    return jsonify({"error": "Title is required"}), 400 # returns 400 if no empty title is provided
  
  # Generate unique event ID
  new_id = max((event.id for event in events), default=0) + 1 # generates unique id higher than existing ids
  
  # Create new Event object
  new_event = Event(new_id, data["title"]) # creates new instance of Event
  
  # Add event to events database
  events.append(new_event) # adds new event to list
  
  # Return new event with 201 status code
  return jsonify(new_event.to_dict()), 201 # returns created event and HTTP 201
  

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
  data = request.get_json(silent=True)
  
  if not isinstance(data, dict) or not isinstance(data.get("title"), str) or not data["title"].strip():
    return jsonify({"error": "Title is required"}), 400
  
  for event in events:
    if event.id == event_id:
      event.title = data["title"]
      return jsonify(event.to_dict()), 200
  return jsonify({"error": "Event not found"}), 404

# # TODO: Task 1 - Define the Problem
# # Remove an event from the list
# @app.route("/events/<int:event_id>", methods=["DELETE"])
# def delete_event(event_id):
#     # TODO: Task 2 - Design and Develop the Code

#     # TODO: Task 3 - Implement the Loop and Process Each Element

#     # TODO: Task 4 - Return and Handle Results
#     pass

if __name__ == "__main__":
    app.run(debug=True)
