#!/bin/bash
while True; do
  echo "Spark is starting"
  docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/spark/spark.py
  echo "Sleep 60"
  sleep 60
done