from pyspark import SparkContext
import json
import urllib
import collections
from itertools import combinations
import urllib.request
import urllib.parse

spkcontext = SparkContext("spark://spark-master:7077", "PopularItems")
data = spkcontext.textFile("/tmp/data/access.log", 2) 
pairs = data.map(lambda line: line.split())
list_pairs = pairs.groupByKey()
list_coview_pairs = list_pairs.flatMap(lambda line: [[line[0], coview] for coview in combinations(list(line[1]), 2)])
reveser_list_coview_pairs = list_coview_pairs.map(lambda pair: (pair[1], pair[0]))
coview_users = reveser_list_coview_pairs.groupByKey()
count_coview = coview_users.map(lambda coview_list: (coview_list[0], len(coview_list[1])))
count_coview_filtered = count_coview.filter(lambda pair: pair[1] >= 3)


f = open("/tmp/data/spark_ouput.log", "w")

output = count_coview_filtered.collect()
table = collections.defaultdict(set)

for pair, count in output:
    f.write(str(pair) + ' ' + str(count) + "\n")
    table[pair[0]].add(pair[1])
    table[pair[1]].add(pair[0])

recommend = {}
for k, v in table.items():
    recommend[k] = ','.join(list(v))

data_encoded = urllib.parse.urlencode({'recommendations': json.dumps(recommend)}).encode('utf-8')
response =  urllib.request.urlopen("http://models:8000/api/v1/recommendation/create/", data_encoded).read().decode('utf-8')
spkcontext.stop()

