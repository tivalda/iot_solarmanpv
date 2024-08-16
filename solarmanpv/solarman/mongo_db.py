import paho.mqtt.client as mqtt
from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import json

# Configuration MQTT
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'votre/topic/iot'

# Configuration MongoDB
def get_client(url='mongodb://root:rootpassword@192.168.33.11:27017/'):
    client = MongoClient(url)
    return client

# Callback appelé lorsque le client reçoit un message du broker MQTT
def mongo_insert(db, collection, message, url=None):
    # Décodage du message MQTT en JSON
    payload = json.loads(message)
    
    # Ajout de l'horodatage
    payload["timestamp"] = datetime.utcnow()
    
    # Insertion du document dans MongoDB
    client = get_client()
    db = client.get_database(db)
    collection = db.get_collection(collection)  
    collection.insert_one(payload)
