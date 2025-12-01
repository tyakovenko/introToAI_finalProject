import pandas as pd
from sklearn.cluster import KMeans
from sklearn import svm
from sklearn.metrics import f1_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
import numpy as np
import random
import json



try:
    with open('all224.json', 'r') as file:
        all224 = json.load(file)

        print("JSON loaded")
        #print(all224)
except FileNotFoundError:
    print("JSON not found")
except json.decoder.JSONDecodeError:
    print("JSON decode error")
except Exception as e:
    print(e)

results = []

labels = []

for i in range(len(all224)):

    result = []
    res = all224[i].get("result")
    labels.append(all224[i].get("label"))
    res1 = 0
    res2 = 0
    for j in range(int (len(res)/2)):
        for k in range(len(res[j])):
            res1 = res1 + res[j][k]
    for j in range(int (len(res)/2), len(res)):
        for k in range(len(res[j])):
            res2 = res2 + res[j][k]
    result.append(res1)
    result.append(res2)
    results.append(result)

resultsTest = []
labelsTest = []

resultsTrain = []
labelsTrain = []

randList = random.sample(range(0, len(results)), int(len(results) * 0.8))
print(randList)
print(len(results))

for i in range(len(randList)):
    if i in randList:
        resultsTest.append(results[i])
        labelsTest.append(labels[i])
    else:
        resultsTrain.append(results[i])
        labelsTrain.append(labels[i])

resultsTrainBegin = []
labelsTrainBegin = []

resultsTrainRecurs = []
labelsTrainRecurs = []

randList2 = random.sample(range(0, int(len(resultsTrain))), int(len(resultsTrain) * 0.8))

for i in range(len(resultsTrain)):
    if i in randList2:
        resultsTrainRecurs.append(resultsTrain[i])
        labelsTrainRecurs.append(labelsTrain[i])
    else:
        resultsTrainBegin.append(resultsTrain[i])
        labelsTrainBegin.append(labelsTrain[i])

p = 0
while(p < 100):
    svcModel = SVC(probability=True, decision_function_shape='ovo')

    svcModel.fit(resultsTrainBegin, labelsTrainBegin)
    #print(svcModel.classes_)


    probs = svcModel.predict_proba(resultsTrainRecurs)
    #print(len(probs))
    #print(len(labelsTrainRecurs))

    resultsTrainRecursNew = []
    labelsTrainRecursNew = []


    for i in range(len(probs)):
        used = False
        #print(probs[i])
        for j in range(len(probs[i])):
            if(probs[i][j] > 0.70):

                resultsTrainBegin.append(resultsTrainRecurs[i])
                labelsTrainBegin.append(j)
                used = True
            elif(j == 2 and used == False):
                #print(i)
                resultsTrainRecursNew.append(resultsTrainRecurs[i])
                labelsTrainRecursNew.append(labelsTrainRecurs[i])

    resultsTrainRecurs = resultsTrainRecursNew[:]
    labelsTrainRecurs = labelsTrainRecursNew[:]

    p += 1

    if(p == 99):
        for i in range(len(probs)):
            largest = 0
            largestIndex = 0
            for j in range(len(probs[i])):
                if(probs[i][j] > largest):
                    largest = probs[i][j]
                    largestIndex = j
            resultsTrainBegin.append(resultsTrain[i])
            labelsTrainBegin.append(largestIndex)


    if(p == 100):
        print(probs)
        preds = svcModel.predict(resultsTest)
        f1 = f1_score(labelsTest, preds, average='macro')
        print(f1)
        accuracy = accuracy_score(labelsTest, preds)
        print(accuracy)