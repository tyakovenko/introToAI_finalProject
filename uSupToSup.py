import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import json



try:
    with open('', 'r') as file:
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


model = KMeans(n_clusters=3).fit(results)
print(model.cluster_centers_)




pred = model.predict(results)

fogsmog = 0
sandstorm = 0
rain = 0

for i in range(len(labels)):
    if(pred[i] == 0 and fogsmog == 0):
        fogsmog = i
    if(pred[i] == 1 and sandstorm == 0):
        sandstorm = i

fogAct = 0
sandAct = 0
rainAct = 0

fog0 = 0
fog1 = 0
fog2 = 0

for i in range(sandstorm):
    if(pred[i] == 1):
        fog1 += 1
    elif(pred[i] == 0):
        fog0 += 1
    else:
        fog2 += 1

if(fog0 > fog1 and fog0 > fog2):
    fogAct = 0
if(fog1 > fog2 and fog1 > fog0):
    fogAct = 1
if(fog2 > fog0 and fog2 > fog1):
    fogAct = 2

rain0 = 0
rain1 = 0
rain2 = 0

for i in range(rain):
    if(pred[i] == 1):
        rain1 += 1
    elif(pred[i] == 0):
        rain0 += 1
    else:
        rain2 += 1

if (rain0 > rain1 and rain0 > rain2):
    rainAct = 0
if (rain1 > rain2 and rain1 > rain0):
    rainAct = 1
if (rain2 > rain0 and rain2 > rain1):
    rainAct = 2

sand0 = 0
sand1 = 0
sand2 = 0

for i in range(sandstorm, rain):
    print(pred[i])
    if(pred[i] == 1):
        sand1 += 1
    elif(pred[i] == 0):
        sand0 += 1
    else:
        sand2 += 1

#print(sand0, sand1, sand2)

if (sand0 > sand1 and sand0 > sand2):
    sandAct = 0
if (sand1 > sand2 and sand1 > sand0):
    sandAct = 1
if (sand2 > sand0 and sand2 > sand1):
    sandAct = 2

print("fog: " + str(fogAct))
print("rain: " + str(rainAct))
print("sand:  " + str(sandAct))