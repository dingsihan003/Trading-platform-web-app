import time
from elasticsearch import Elasticsearch
import collections
import os
from kafka import KafkaConsumer

es = Elasticsearch(['es'])
length = 0
id_list = []
def update_counts():
  global length
  global id_list
  if os.stat("/tmp/data/access.log").st_size == 0:
    print('an empty file')
    return
  # if os.stat("/tmp/data/access.log").st_size == length:
  #   print('No new thing added')
  #   return
  print(length)
  length = os.stat("/tmp/data/access.log").st_size
  f = open("/tmp/data/access.log", "r")
  c = collections.defaultdict(set)
  for line in f.readlines():
    print(line)
    user_id, item_id  = line.split()
    if item_id not in id_list:
      id_list.append(item_id)
      es.update(index='listing_index', doc_type='listing', id=item_id , body={ 'script' : 'ctx._source.visits = 0'})
      es.update(index='listing_index', doc_type='listing', id=item_id , body={ 'script' : 'ctx._source.visits += 1'})
    else:
      print(item_id)
      es.update(index='listing_index', doc_type='listing', id=item_id , body={ 'script' : 'ctx._source.visits += 1'})
  with open("/tmp/data/access.log", "w"):
    pass
  f.close()

while True:
  update_counts()
  time.sleep(60)