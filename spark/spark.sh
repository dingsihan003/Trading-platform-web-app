#!/bin/bash
while True; do
  echo "Start spark"
  docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/spark/spark.py
  echo "Sleep for 60 seconds"
  sleep 60
done