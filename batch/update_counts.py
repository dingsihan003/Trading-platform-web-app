import time
from elasticsearch import Elasticsearch
import collections
import os
from kafka import KafkaConsumer

es = Elasticsearch(['es'])

while True:
  if os.stat("/tmp/data/access.log").st_size == 0:
    return
  f = open("/tmp/data/access.log", "r")
  c = collections.defaultdict(set)
  for line in f.readlines():
    user_id, item_id  = line.split()
    c[item_id].add(user_id)
  for item_id, users in c.items():
    print(item_id, len(users))
    es.update(index='listing_index', doc_type='listing', id=item_id , body={ 'script' : 'ctx._source.visits = 0'})
    try:
      for i in range(len(users)):
        es.update(index='listing_index', doc_type='listing', id=item_id , body={ 'script' : 'ctx._source.visits += 1'})
    except Exception as e:
      print(str(e))
      time.sleep(1)
  f.close()
  time.sleep(60)