
from flask import Flask, jsonify
from sklearn import svm
import numpy as np
import os.path
import re as re

#TweetTokens = nltk.pos_tag(nltk.word_tokenize(inputTweet)) 
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://ffqrdev_writer:Heechou1@esgen01deva04:9201'],verify=False)

from sklearn.externals import joblib
clf = svm.SVC() 
clf = joblib.load('dumptrain.pkl') 


import xlrd
book = xlrd.open_workbook(os.path.join('C:\\Users\\rachanti\\Desktop\\Course\\twitter','sa_tweets-trng-data-for-model-v2b.xlsx'))
sheet = book.sheets()[0]
import nltk
#nltk.download()
#import matplotlib.pyplot as plt
#from matplotlib.colors import Normalize
app = Flask(__name__)
@app.route('/svm', methods = ['GET'])
def vectorpredict():
       X=[]
       y=[]
       vscore =[]
       inputTweet=''
       #for i in range(sheet.nrows):
       #     inputTweet = sheet.row_values(i)[8]
       #     inputTweet = re.sub(r"http\S+",'',inputTweet)
       #     inputTweet = re.sub(r"#\S+",'',inputTweet)
       #     inputTweet = re.sub(r".*:",'',inputTweet) 
          
       #     TweetTokens = nltk.pos_tag(nltk.word_tokenize(inputTweet)) 
       #     NTweet = ''

       #     for word in TweetTokens:
       #         if word[1] in ['NNP','NN','NNS']:
       #             NTweet = NTweet +' '+ word[0]
             
                                  
       #     vscore = GetTrainVector(NTweet)
       #     if vscore !=[0,0,0,0,0,0,0,0,0]:
       #       X.append(vscore)
       #       if (sheet.row_values(i)[4] == ''):
       #           y.append(0)
       #       else :
       #           y.append(1)
              
        
        
       #X = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0.06066217300000001,
       #0.06825315824999999,
       #0.07663112727272726,
       #0.05768009730769231,
       #0.06382067525,
       #0.0637208,
       #0.0644870868,
       #0.09019162700000001,
       #0.06328284975],[0.12604570164705883,
       #0.13160675388888887,
       #0,
       #0.14012992200000002,
       #0.17688938377358493,
       #0.1798896,
       #0.13165299375,
       #0,
       #0.079958744]]
       #y = [0,0, 1]

       from sklearn.externals import joblib
       clf = svm.SVC()       
       #clf.fit(X, y)        
       #joblib.dump(clf, 'dumptrain.pkl')
          #SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
          #  decision_function_shape=None, degree=3, gamma='auto',
          #  kernel='rbf',
          #  max_iter=-1, probability=False, random_state=None, shrinking=True,
          #  tol=0.001, verbose=False)

       clf = joblib.load('dumptrain.pkl') 
       a = clf.predict([
0.0611111014,
0.0611111014,
0.0611111014,
0.08254474992307693,
0,
0.079347514,
0.10223679808333332,
0.07709919716666667,
0.080045527,
0.061155535,
0
])
          #return jsonify(a)
       print(a)

   

#  plt.figure(figsize=(8, 6))
@app.route('/predict/<list>', methods = ['GET'])
def Predict(list):  
       #clf = joblib.load('dumptrain.pkl') 
       #list = re.findall(r'"\s*([^"]*?)\s*"', list)
       a = clf.predict(eval(list))
       x=[]
       x.append(a[0])
       return jsonify(str(x[0]))

@app.route('/<desc>', methods = ['GET'])
def GetTrainVector(desc):
     vectorscore = []
     count = {}
     res = es.search(index="cace" ,doc_type = "current-affairs",size=100,body={"query": {"match": {"content": desc}}})
     #count = Counter([d['_source']['category'] for d in res['hits']['hits']])
     categories = ['Armed conflicts and attacks','Politics and elections','Disasters and accidents','Law and crime','International relations','Business and economy','Arts and culture','Sports','Science and technology']
     for cat in categories :
        if cat == "Business and economy":
          a = list(filter(lambda d :(d['_source']['category'] == cat or d['_source']['category'] == 'Business and economics' ),res['hits']['hits']))  
        else:
          a = list(filter(lambda d :(d['_source']['category'] == cat),res['hits']['hits']))           
        if(len(a) == 0):
          v = 0
        else:
          #s = max(item['_score'] for item in a)
          #v = s / len(a)
          s= a[0]['_score']
          if (s>=0.2):
            v=s
          else:
            v=0
        vectorscore.append(v)

     return jsonify(vectorscore)
     #return vectorscore



if __name__ == '__main__':
    port = 7003 #the custom port you want
    app.run(host='127.0.0.1', port=port)















#def vector():
## we create 40 separable points
#    np.random.seed(0)
#    X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2,
#    2]]
#    Y = [0] * 20 + [1] * 20
    
#    # figure number
#    fignum = 1
    
#    # fit the model
#    for name, penalty in (('unreg', 1), ('reg', 0.05)):
    
#        clf = svm.SVC(kernel='linear', C=penalty)
#        clf.fit(X, Y)
    
#        # get the separating hyperplane
#        w = clf.coef_[0]
#        a = -w[0] / w[1]
#        xx = np.linspace(-5, 5)
#        yy = a * xx - (clf.intercept_[0]) / w[1]
    
#        # plot the parallels to the separating hyperplane that pass through
#        the
#        # support vectors
#        margin = 1 / np.sqrt(np.sum(clf.coef_ ** 2))
#        yy_down = yy + a * margin
#        yy_up = yy - a * margin
    
#        # plot the line, the points, and the nearest vectors to the plane
#        plt.figure(fignum, figsize=(4, 3))
#        plt.clf()
#        plt.plot(xx, yy, 'k-')
#        plt.plot(xx, yy_down, 'k--')
#        plt.plot(xx, yy_up, 'k--')
    
#        plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
#        s=80,
#                    facecolors='none', zorder=10)
#        plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired)
    
#        plt.axis('tight')
#        x_min = -4.8
#        x_max = 4.2
#        y_min = -6
#        y_max = 6
    
#        XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
#        Z = clf.predict(np.c_[XX.ravel(), YY.ravel()])
    
#        # Put the result into a color plot
#        Z = Z.reshape(XX.shape)
#        plt.figure(fignum, figsize=(4, 3))
#        plt.pcolormesh(XX, YY, Z, cmap=plt.cm.Paired)
    
#        plt.xlim(x_min, x_max)
#        plt.ylim(y_min, y_max)
    
#        plt.xticks(())
#        plt.yticks(())
#        fignum = fignum + 1
    
#    plt.show()


if __name__ == '__main__':
    vectorpredict()
    #port = 7001 #the custom port you want
    #app.run(host='127.0.0.1', port=port)
