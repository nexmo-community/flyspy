from flask import Flask, jsonify, request
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB('db4.json')

@app.route("/", methods=['GET'])
def index():
  evt = Query()
  obj = db.search(evt.location != '')  
  return (jsonify(obj))

@app.route("/events", methods=['GET'])
def get_all_events():
  evt = Query()
  return (jsonify(db.search(evt.location != '')))

# Gets events with this sevrity or greater
@app.route("/events/<int:severity>", methods=['GET'])
def get_events_with_severity(severity):
  evt = Query()
  return (jsonify(db.search((evt.location != '') & (evt.severity >= severity) )))

@app.route("/add", methods=['POST'])
def add_event():
  
  data = request.get_json()
  print(data)
  
  location = data['location']
  url = data['url']
  description = data['description']
  severity = data['severity']
  
  obj = {'location': location, 'url': url, 'description': description, 'severity': severity }
  print(obj)
  db.insert(obj)
  
  return ("200")

if __name__ == "__main__":
  app.run()
