from google.cloud import pubsub_v1 as ps
from concurrent import futures
from datetime import datetime
import time
import threading
from dotenv import load_dotenv
import os

# Loading environment variables from .env file
load_dotenv()
PROJECT_ID =  os.getenv("PROJECT_ID")
TOPIC = os.getenv("TOPIC1")


# Configuring the the batch to 10 seconds latency.
batch_settings = ps.types.BatchSettings(
    max_latency=10,
    # max_messages=,
    # max_bytes=
)


# Initializing the publisher client
publisher = ps.PublisherClient(batch_settings)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)
publish_futures = []


# Resolving the publish future in a separate thread
def callback(future: ps.publisher.futures.Future) -> None:
    message_id = future.result()
    print(f'Got {message_id}.')

n = 1
try:
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_str = f'Message number {n}\n Timestamp {current_time}.'
        # Converting the data to a bytestring
        data = data_str.encode('utf-8')
        publish_future = publisher.publish(topic_path, data)
        # Allowing the publisher client to batch multiple messages.
        publish_future.add_done_callback(callback)
        publish_futures.append(publish_future)
        time.sleep(1.5)
        n += 1

except KeyboardInterrupt:
    print("User halted the publish process")

futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
print(f'Published messages with batch settings to {topic_path}.')
