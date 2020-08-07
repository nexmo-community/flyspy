from flask import Flask, request, jsonify
from pprint import pprint

app = Flask(__name__)

url = None

def write_event_file (location, description, image_url):
    evt = { 'location': location, 'description': description, 'image_url': image_url}
    # writes the object to a file, one line per object
    with open ('log.txt', 'a') as f:
        s = "%s|%s|%s\n" % (location, description, image_url)
        f.write(s)
    return

def read_events_file ():
    events = []
    # open file and read events
    with open ('log.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            location, description, image_url = line.split('|') 
            obj = { 'location': location, 'description': description, 'image_url': image_url}
            events.append(obj)
        return events    

## API

@app.route("/", methods=['GET'])
def index():
    print('Fly spy')
    return ('Welcome to Fly Spy', 200)

@app.route("/event", methods=['GET'])
def get_event():
    print('You requested last event...')
    headers = {}  
    headers['Access-Control-Allow-Origin'] = '*'
    events = []
    events = read_events_file()
    event = events.pop()
    return (jsonify(event), headers)

@app.route("/events", methods=['GET'])
def get_events():
    print('You requested events...')
    headers = {}  
    headers['Access-Control-Allow-Origin'] = '*'
    return (jsonify(read_events_file()), headers)

## Application-level webhooks

@app.route("/webhooks/inbound", methods=['POST'])
def inbound():
    global url
    data = request.get_json()
    pprint(data) 
    type = data['message']['content']['type']
    if type == 'image':
        url = data['message']['content']['image']['url']
        print(url)
    elif type == 'text':
        m = data['message']['content']['text'].strip()
        if m.lower() == 'help':
            # send help message back to user
            print('Send image followed by location: description')
        else:
            location, description = m.split(':')
            location = location.upper().strip()
            description = description.strip()
            if url:
                write_event_file(location, description, url)
                url = None
    return (jsonify(data))

@app.route("/webhooks/status", methods=['POST'])
def status():
    data = request.get_json()
    pprint(data) 
    return (jsonify(data))

if __name__ == "__main__":
  app.run()
