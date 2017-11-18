from collections import Counter
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://ffqrdev_writer:Heechou1@esgen01deva04:9201'],verify=False)
#if not es.ping():
#    res= es.search(index="logs" ,doc_type = "performance",body={"query": {"match_all": {}}})
#    for doc in res['hits']['hits']:
#        print ("%s"%doc['_id'])
import nltk
import re as re

from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/<desc>', methods = ['GET'])
def vector(desc):
     inputTweet = desc
     inputTweet = re.sub(r"http\S+",'',inputTweet)
     inputTweet = re.sub(r"#\S+",'',inputTweet)
     inputTweet = re.sub(r".*:",'',inputTweet) 
   
     TweetTokens = nltk.pos_tag(nltk.word_tokenize(inputTweet)) 
     NTweet = ''

     for word in TweetTokens:
         if word[1] in ['NNP','NN','NNS']:
             NTweet = NTweet +' '+ word[0]

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
        #vectorscore.append(NTweet)
     return jsonify(vectorscore)
     #print (dict(count))
     #for doc in res['hits']['hits']:
     #   print ("%s"% doc['category'])


@app.route('/ngram/<desc>', methods = ['GET'])
def vector1(desc):
     inputTweet = desc
     inputTweet = re.sub(r"http\S+",'',inputTweet)
     inputTweet = re.sub(r"#\S+",'',inputTweet)
     inputTweet = re.sub(r".*:",'',inputTweet) 
   
     TweetTokens = nltk.pos_tag(nltk.word_tokenize(inputTweet)) 
     NTweet = ''

     for word in TweetTokens:
         if word[1] in ['NNP','NN','NNS']:
             NTweet = NTweet +' '+ word[0]

     vectorscore =[]
     #count ={}
     #res= es.search(index="cace" ,doc_type = "current-affairs",size=100,body={"query": {"match": {"content": desc}}})
     ##count = Counter([d['_source']['category']  for d in res['hits']['hits']])
     #categories = ['Armed conflicts and attacks','Politics and elections','Disasters and accidents','Law and crime','International relations','Business and economy','Arts and culture','Sports','Science and technology']
     #for cat in categories :
     #   a = list(filter(lambda d :(d['_source']['category'] == cat),res['hits']['hits'] ))
        
     #   if(len(a)==0):
     #     v=0
     #   else:
     #     s = sum(item['_score'] for item in a)
     #     v=  s/len(a)
     #   vectorscore.append(v)
     vectorscore.append(NTweet)
     return jsonify(vectorscore)
     #print (dict(count))
     #for doc in res['hits']['hits']:
     #   print ("%s"% doc['category'])


if __name__ == '__main__':
    port = 7001 #the custom port you want
    app.run(host='127.0.0.1', port=port)