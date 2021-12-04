import os
import pickle
import cv2
import json
from json import JSONEncoder
from celery import Celery
import numpy

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

app = Celery('server2',broker='amqps://xplxppkm:HRzEUgmldTlk4UUwjzks4K4cqmpk37jf@toad.rmq.cloudamqp.com/xplxppkm')

@app.task
def passToServer2(serializedFiles,fileNames):
    finalNumpyArrays=[]
    arrayToMergeServer = []
    booleanArray = []
    folder=[]
    print (len(serializedFiles))
    for x in range(len(serializedFiles)):
        decodedArrays = json.loads(serializedFiles[x])
        finalNumpyArrays.append(numpy.asarray(decodedArrays[fileNames[x]]))
    
    for x in range (len(fileNames)):
        fileNames[x]=''.join([i for i in fileNames[x] if not i.isdigit()])
        fileNames[x] = fileNames[x].split('.')[0]
        print(fileNames[x])
    for x in range (len(fileNames)):
        booleanArray.append(False)
    for i in range(len(fileNames)):
        if booleanArray[i]==False:
            arrayToMergeServer.append([serializedFiles[i]])
            booleanArray[i]=True
        else:
            continue
        for j in range(i + 1, len(fileNames)):
            if(fileNames[i].casefold()==fileNames[j].casefold()):
                if booleanArray[j]==False:
                    arrayToMergeServer[i].append(serializedFiles[j])
                    booleanArray[j]=True
    print("LENGTH "+str(len(arrayToMergeServer[0])))

