from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['webhookDB']
collection = db['webhook_events']

# Home route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        data['timestamp'] = datetime.utcnow()
        collection.insert_one(data)
    return 'Webhook received', 200

# Route to fetch data from MongoDB
@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    # Remove ObjectId before sending
    for event in events:
        event['_id'] = str(event['_id'])
    return {'events': events}

if __name__ == '__main__':
    app.run(debug=True)
