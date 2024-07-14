from google.cloud import pubsub_v1
import time
import threading
from dotenv import load_dotenv
import os

# Loading environment variables from .env file
load_dotenv()
PROJECT_ID =  os.getenv("PROJECT_ID")
TOPIC = os.getenv("TOPIC1")


# Initializing the publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)

print(topic_path)