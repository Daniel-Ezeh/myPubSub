import time
import datetime
from google.cloud import pubsub_v1

project_id = ""
topic_name = ""


publisher = pubsub_v1.PublisherClient()