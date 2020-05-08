import time
from elasticsearch import Elasticsearch
import collections
import os
from kafka import KafkaConsumer
es = Elasticsearch(['es'])

def update_counts():
  if os.stat("/tmp/data/access.log").st_size == 0:
    print('an empty file')
    return
  f = open("/tmp/data/access.log", "r")
  c = collections.defaultdict(set)
  for line in f.readlines():
    user, item  = line.split()
    c[item].add(user)
  for item, users in c.items():
    es.update(index='listing_index', doc_type='listing', id=item , body={ 'script' : 'ctx._source.visits = 0'})
    try:
      for i in range(len(users)):
        es.update(index='listing_index', doc_type='listing', id=item , body={ 'script' : 'ctx._source.visits += 1'})
    except Exception as e:
      print(str(e))
      time.sleep(1)
  f.close()
while True:
  update_counts()
  time.sleep(60)