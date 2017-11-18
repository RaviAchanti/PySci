from collections import Counter
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://ffqrdev_writer:Heechou1@esgen01deva04:9201'],verify=False)
#if not es.ping():
#    res= es.search(index="logs" ,doc_type = "performance",body={"query": {"match_all": {}}})
#    for doc in res['hits']['hits']:
#        print ("%s"%doc['_id'])

from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/<desc>', methods = ['GET'])
def vector(desc):
  
     vectorscore =[]
     count ={}
     res= es.search(index="cace" ,doc_type = "current-affairs",size=100,body={"query": {"match": {"content": desc}}})
     #count = Counter([d['_source']['category']  for d in res['hits']['hits']])
     categories = ['Armed conflicts and attacks','Politics and elections','Disasters and accidents','Law and crime','International relations','Business and economy','Arts and culture','Sports','Science and technology']
     for cat in categories :
        a = list(filter(lambda d :(d['_source']['category'] == cat),res['hits']['hits'] ))
        
        if(len(a)==0):
          v=0
        else:
          s = sum(item['_score'] for item in a)
          v=  s/len(a)
        vectorscore.append(v)
     return jsonify(vectorscore)
     #print (dict(count))
     #for doc in res['hits']['hits']:
     #   print ("%s"% doc['category'])


if __name__ == '__main__':
    port = 7001 #the custom port you want
    app.run(host='127.0.0.1', port=port)


#Someone named TOM TAYLOR to play JAKE CHAMBERS in THE DARK TOWER.
#[
#0.06066217300000001,
#0.06825315824999999,
#0.07663112727272726,
#0.05768009730769231,
#0.06382067525,
#0.0637208,
#0.0644870868,
#0.09019162700000001,
#0.06328284975
#]

#Interested
#China urges diplomats and U.N. to boycott Dalai Lama in Geneva
#[
#0.12604570164705883,
#0.13160675388888887,
#0,
#0.14012992200000002,
#0.17688938377358493,
#0.1798896,
#0.13165299375,
#0,
#0.079958744
#]
