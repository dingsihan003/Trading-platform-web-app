from pyspark import SparkContext
from itertools import combinations
import urllib.request
import urllib.parse
import json
import urllib
import collections

# user id, item id
sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file
# 1. Read data in as pairs of (item_id clicked on by the user, user_id )
# print('data,,,,,..........', data.take(3))
# print(data)
pairs = data.map(lambda line: line.split())   # tell each worker to split each line of it's partition
# print('pairs...............', pairs.take(3))

# 2. Group data into (user_id, list of item ids they clicked on)
list_pairs = pairs.groupByKey()
# print('list_pairs...............', list_pairs.take(3))

# 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
list_coview_pairs = list_pairs.flatMap(lambda line: [[line[0], coview] for coview in combinations(list(line[1]), 2)])
# print('list_coview_pairs', list_coview_pairs.take(3))
# 4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
reveser_list_coview_pairs = list_coview_pairs.map(lambda pair: (pair[1], pair[0]))
# print('reveser_list_coview_pairs............', reveser_list_coview_pairs.take(3))

coview_users = reveser_list_coview_pairs.groupByKey()
# print('coview_users,,,,,,,,,,,,,,,,', coview_users.take(3))

# 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
count_coview = coview_users.map(lambda coview_list: (coview_list[0], len(coview_list[1])))
# print('hhhhh', count_coview.take(3))
# 6. Filter out any results where less than 3 users co-clicked the same pair of items
count_coview_filtered = count_coview.filter(lambda pair: pair[1] >= 3)

output = count_coview_filtered.collect()
print(output)
                    # bring the data back to the master node so we can print it out
f = open("/tmp/data/spark_ouput.log", "w")

table = collections.defaultdict(set)

for pair, count in output:
    print ("pair %s count %d" % (pair, count))
    f.write(str(pair) + ' ' + str(count) + "\n")
    table[pair[0]].add(pair[1])
    table[pair[1]].add(pair[0])
recommendations = {}
for k, v in table.items():
    recommendations[k] = ','.join(list(v))
print(recommendations)
print ("Popular items done")

post_value = {
  'recommendations': json.dumps(recommendations)
}
post_encoded = urllib.parse.urlencode(post_value).encode('utf-8')
print(post_encoded)
# try:
response =  urllib.request.urlopen("http://models:8000/api/v1/recommendation/create/", post_encoded).read().decode('utf-8')
print(response)
sc.stop()

