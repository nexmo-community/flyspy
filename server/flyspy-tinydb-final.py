from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from pprint import pprint

app = Flask(__name__)

db = TinyDB('db.json')
url = None

## API

@app.route("/", methods=['GET'])
def index():
    print('Fly spy')
    return ('Welcome to Fly Spy - TinyDB version', 200)

# Get event with severity  
@app.route("/events/<int:severity>", methods=['GET'])
def get_events_with_severity(severity):
    headers = {}  
    headers['Access-Control-Allow-Origin'] = '*'
    evt = Query()
    return (jsonify(db.search((evt.location != '') & (evt.severity == severity) )))

# Get all events  
@app.route("/events", methods=['GET'])
def get_events():
    headers = {}  
    headers['Access-Control-Allow-Origin'] = '*'
    evt = Query()
    return (jsonify(db.search(evt.location != '')), headers)

  
## Application-level webhooks

@app.route("/webhooks/inbound", methods=['POST'])
def inbound():
    global url
    data = request.get_json()
    pprint(data) 
    type = data['message']['content']['type']
    if type == 'image':
        url = data['message']['content']['image']['url']
    elif type == 'text':
        m = data['message']['content']['text'].strip()
        if m.lower() == 'help':
            # send help message back to user
            print('Send image followed by location: description')
        else:
            location, description, severity = m.split(':')
            location = location.upper().strip()
            description = description.strip()
            severity = int(severity.strip())
            if url:
                # write record to database
                obj = {'location': location, 'url': url, 'description': description, 'severity': severity }
                db.insert(obj)
                url = None
    return (jsonify(data))

@app.route("/webhooks/status", methods=['POST'])
def status():
    data = request.get_json()
    pprint(data) 
    return (jsonify(data))

if __name__ == "__main__":
  app.run()
