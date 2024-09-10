import time
from datetime import datetime
from google.cloud import pubsub_v1


# Getting the project_id and topic_name
# command1 = "gcloud config get-value project"
# project_id = subprocess.run(command1, shell=True, capture_output=True, text=True)
project_id = "trying-pubsub-2024"

# command2 = 'gcloud pubsub topics list | grep "my" | rev | cut -d\'/\' -f1 | rev'
# topic_name  = subprocess.run(command2, shell=True, capture_output=True, text=True)
topic_name = "myTopic"

# Initializing a publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

def publish_message(message):
    # Publishes a message to the Pub/Sub topic
    future = publisher.publish(topic_path, data=message.encode('utf-8'))
    print(f"Published message: {message}")
    future.result() # Waits for the message to be published

try:
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        publish_message(current_time)
        time.sleep(11.5) #Publishes every 11.5 seconds

except KeyboardInterrupt:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Publisher stopped at {current_time}")



