from kafka import KafkaConsumer
import json
import time
f = open("/tmp/data/access.log", "a")
while(True):
    try:
        consumer = KafkaConsumer('log', group_id='log-counter', bootstrap_servers=['kafka:9092'])
        print("log consumer",consumer)
        break
    except:
        print("log consumer failed")
        time.sleep(3)
for message in consumer:
    message_json = json.loads(message.value.decode("utf-8"))
    f.write(str(message_json['user_name']) + ' ' + str(message_json['item_id']) + "\n")
    f.flush()