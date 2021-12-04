import os
import pickle
import cv2
import json
from json import JSONEncoder
from celery import Celery
import numpy
from server_1_task import passToServer1
from server_2_task import passToServer2
from server_3_task import passToServer3

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
def merge(serialized_arrayOfFolders,nameOfFolders):
    print("merging")
    global counter
    
    allFolders= []
    allFolderNames=[]
    # booleanArray = []
    # server1Folders= []
    # server2Folders = []
    # server3Folders = []
    # server1FoldersNames= []
    # server2FoldersNames = []
    # server3FoldersNames = []
    # if counter==0:
    #     server1Folders = serialized_arrayOfFolders
    #     server1FoldersNames = nameOfFolders
    # elif counter==1:
    #     server2Folders = serialized_arrayOfFolders
    #     server2FoldersNames = nameOfFolders
    # elif counter==2:
    #     server3Folders = serialized_arrayOfFolders
    #     server3FoldersNames = nameOfFolders
    # counter+=1
    # if counter>=3:
    #     for x in range(len(server1Folders)):
    #         allFolders.append(server1Folders[x])
    #         allFolderNames.append(server1FoldersNames[x])
    #     for x in range(len(server2Folders)):
    #         allFolders.append(server2Folders[x])
    #         allFolderNames.append(server2FoldersNames[x])
    #     for x in range(len(server3Folders)):
    #         allFolders.append(server3Folders[x])
    #         allFolderNames.append(server3FoldersNames[x])

    #     processingArray = allFolders
    #     for i in range(len(allFolders)):
    #         for j in range(i + 1, len(allFolders)):
    #             if(allFolderNames[i]==allFolderNames[j]):
    #                 processingArray[i].append
    # for x in range(len(serialized_arrayOfFolders)):
    #     allFolders.append(serialized_arrayOfFolders[x])
    #     allFolderNames.append(nameOfFolders[x])

    # if counter<3:
    #     print("sadskjas")
    #     counter+=1
    # else:
    #     return allFolders,allFolderNames

def divide_workload(directory):
    path, dirs, files = next(os.walk(directory))
    imageCount=0
    server_1_files = []
    server_2_files = []
    server_3_files = []
    server_1_file_names = []
    server_2_file_names = []
    server_3_file_names = []
    server_1_files_arrays=[]
    server_2_files_arrays=[]
    server_3_files_arrays=[]
    server_1_files_serialized=[]
    server_2_files_serialized=[]
    server_3_files_serialized=[]

    

    for file in files:
        if (file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.jfif') or file.endswith('.bmp')):
            imageCount +=1
            #print(path+"\\"+file)
    print('count: '+str(imageCount))
    for x in range(imageCount//3):
        server_1_files.append(path+"\\"+files[x])
        server_2_files.append(path+"\\"+files[x+(imageCount//3)])
        server_3_files.append(path+"\\"+files[x+((imageCount//3)*2)])
    if(imageCount%3!=0):
        for x in range (imageCount%3):
            server_3_files.append(path+"\\"+files[x+((imageCount//3)*3)])

    

    for x in range(len(server_1_files)):
        server_1_files_arrays.append(cv2.imread(server_1_files[x]))
        key="array"+str(x)
        key1 = files[x]
        print('SERVER 1'+key)
        print(key1)
        server_1_file_names.append(key1)
        numpyData = {key1: server_1_files_arrays[x]}
        server_1_files_serialized.append(json.dumps(numpyData,cls=NumpyArrayEncoder))
        print("run"+str(x))

    for x in range(len(server_2_files)):
        server_2_files_arrays.append(cv2.imread(server_2_files[x]))
        key="array"+str(x)
        key1 = files[x+(imageCount//3)]
        print('SERVER 2'+key)
        print(key1)
        server_2_file_names.append(key1)
        numpyData = {key1: server_2_files_arrays[x]}
        server_2_files_serialized.append(json.dumps(numpyData,cls=NumpyArrayEncoder))
        print("run"+str(x))


    for x in range(len(server_3_files)):
        server_3_files_arrays.append(cv2.imread(server_3_files[x]))
        key="array"+str(x)
        key1 = files[x+((imageCount//3)*2)]
        print('SERVER 3'+key)
        print(key1)
        server_3_file_names.append(key1)
        numpyData = {key1: server_3_files_arrays[x]}
        server_3_files_serialized.append(json.dumps(numpyData,cls=NumpyArrayEncoder))
        print("run"+str(x))
    
    passToServer1.delay(server_1_files_serialized,server_1_file_names)
    print("passed to server one and processed")
    passToServer2.delay(server_2_files_serialized,server_2_file_names)
    print("passed to server two and processed")
    passToServer3.delay(server_3_files_serialized,server_3_file_names)
    print("passed to server three and processed")
    

    