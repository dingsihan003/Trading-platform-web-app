from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
es = Elasticsearch(['es'])
import json
import time
while(True):
    try:
        consumer = KafkaConsumer('listing', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        break
    except:
        time.sleep(3)
for message in consumer:
    message_json = json.loads(message.value.decode("utf-8"))
    print(message_json)
    while(not es.ping()):
        time.sleep(3)
    es.index(index='listing_index', doc_type='listing', id=message_json['id'], body=message_json)
    es.indices.refresh(index="listing_index")