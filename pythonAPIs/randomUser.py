import os
from dotenv import load_dotenv
import requests
from pprint import pprint
import time
from datetime import datetime
from google.cloud import pubsub_v1 as ps

load_dotenv()

API = os.getenv('API_KEY')
PROJECT_ID =  os.getenv("PROJECT_ID")
TOPIC = os.getenv("TOPIC1")

def get_user():
    """
    Fetch the random user API
    """
    # Endpoint URL for the weather API
    url = f'https://api.api-ninjas.com/v1/randomuser'
    try:
        # Send GET request to the API
        response = requests.get(url, headers={'X-Api-Key': API})
        response.raise_for_status() 
        data = response.json()
        myDict = dict(
        username = data['username'],
        fullname = data['name'],
        address = data['address'],
        email = data['email'],
        gender = data['sex'],
        birthday = data['birthday']
        )
        return str(myDict)
    
    except requests.exceptions.RequestException as e:
        # Handle connection errors or bad responses
        print("Error getting user:", e)
        return None


publisher = ps.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)

def publish_message(message):
    # Publishes a message to the Pub/Sub topic
    future = publisher.publish(topic_path, data=message.encode('utf-8'))
    print(f"Published message: {message}")
    future.result() # Waits for the message to be published


try:
    while True:
        mess = get_user()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        publish_message(mess)
        time.sleep(11.5) #Publishes every 11.5 seconds

except KeyboardInterrupt:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Publisher stopped at {current_time}")