import requests
import json
from bs4 import BeautifulSoup

from flask import Flask, jsonify

app = Flask(__name__)
@app.route('/', methods = ['GET'])

def samplefunction():
    #access your DB get your results here
    #data = {"data":"Processed Data"}
    url = "https://en.wikipedia.org/wiki/Portal:Current_events/January_2010"
    response = requests.get(url)
    html = response.content
    
    soup = BeautifulSoup(html)
    tables = soup.find_all("table" ,class_="vevent")
    
    #print (table.prettify())
    list1=[]
    list2 ={}
    list3 ={}
    list4 =[]
    for table in tables:
        list2 ={}
        date = table.find_all("span" , class_ = "summary")        
        #list2['date']= date[0].text
        topics = table.find_all("dt")
        list3 ={}
        for topic in topics:    
          list4=[]        
          #list3.append(topic.text)
          desc = topic.find_next("ul")
          #list4.append(desc.text)
          list3[topic.text]=desc.text
         
        list2[date[0].text] =list3
        list1.append(list2)
    return jsonify(list1)

if __name__ == '__main__':
    port = 8001 #the custom port you want
    app.run(host='127.0.0.1', port=port)


#url = "http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html"
#response = requests.get(url)
#html = response.content

#soup = BeautifulSoup(html)
#table = soup.find_all('p')

#for row in table:
#    print(row.text)

#Working stuff

#url = "https://en.wikipedia.org/wiki/Portal:Current_events#2017_January_18"
#response = requests.get(url)
#html = response.content

#soup = BeautifulSoup(html)
#tables = soup.find_all("table" ,class_="vevent")

##print (table.prettify())
#list1=[]
#list2 =[]
#list3 =[]
#list4 =[]
#for table in tables:
#         list2 =[]
#         date = table.find_all("span" , class_ = "summary")        
#         list2.append(date[0].text)
#         topics = table.find_all("dt")
#         list3 =[]
#         for topic in topics:    
#          list4=[]        
#          list3.append(topic.text)
#          desc = topic.find_next("ul")
#          list4.append(desc.text)
#          list3.append(list4)
          
#         list2.append(list3)
#         list1.append(list2)
         
#         #list3.append(table.find_all("li"))

#print ( json.dumps(list1,indent = 4))
   

