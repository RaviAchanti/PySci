#class Extract(object):
#    """description of class"""
#    def __init__(self, *args, **kwargs):
#        return super(Extract, self).__init__(*args, **kwargs)


#from collections import namedtuple
#wikiextract = namedtuple('wikiextract','category content date url')

#x= wikiextract('Arts','Mona Lisa','26th jan', 'yahoo.com')

import requests
import json
import uuid
from bs4 import BeautifulSoup
from collections import namedtuple
wikiextract = namedtuple('wikiextract','category content date url')

from elasticsearch import Elasticsearch
es = Elasticsearch(['http://ffqrdev_writer:Heechou1@esgen01deva04:9201'],verify=False)
#if not es.ping():
#    res= es.search(index="logs" ,doc_type = "performance",body={"query": {"match_all": {}}})
#    for doc in res['hits']['hits']:
#        print ("%s"%doc['_id'])

from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/', methods = ['GET'])
def samplefunction():
    #access your DB get your results here
    #data = {"data":"Processed Data"}
    months =['January','February','March','April','May','June','July','August','September','October','November','December']
    #months =['January']
    list1=[]
    for month in months :
       url = "https://en.wikipedia.org/wiki/Portal:Current_events/" + month +"_2012"
       response = requests.get(url)
       html = response.content
       
       soup = BeautifulSoup(html)
       tables = soup.find_all("table" ,class_="vevent")
       
       #print (table.prettify())
   
       
       for table in tables:
           date = table.find_all("span" , class_ = "summary")        
           topics = table.find_all("dt")
           for topic in topics:    
             desclist = topic.find_next("ul")
             for desc in desclist.find_all("li"):
                link = desc.find_next("a",class_="external text") 
                x= wikiextract(category=topic.text,content=desc.text,date=date[0].text,url=link['href'])
                list1.append(x._asdict())
                es.create(index="cace",doc_type="current-affairs",body={"category":x[0],"content":x[1],"date":x[2],"url":x[3]},id =uuid.uuid4())

          
              
            
           #list2[date[0].text] =list3
       #print (x._asdict())
    return jsonify(list1)

if __name__ == '__main__':
    port = 8001 #the custom port you want
    app.run(host='127.0.0.1', port=port)





