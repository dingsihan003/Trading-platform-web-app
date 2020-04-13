from kafka import KafkaConsumer
import json
import time

while(True):
    try:
        consumer = KafkaConsumer('log', group_id='log-counter', bootstrap_servers=['kafka:9092'])
        break
    except:
        time.sleep(3)
for message in consumer:
    f = open("/tmp/data/access.log", "a")
    message_json = json.loads(message.value.decode("utf-8"))
    f.write(str(message_json['user_name']) + ' ' + str(message_json['item_id']) + "\n")
    f.flush()
    f.close()
