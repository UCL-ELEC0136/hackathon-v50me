import pymongo
from pprint import pprint
from random import randint
import requests
import numpy as np
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb+srv://student:assignment@daps2022.l7mstiw.mongodb.net/?retryWrites=true&w=majority")
db = client.hackathon
col = db.google_stars

link = "https://api.github.com/orgs/google/repos?page="
repos = []
i = 1
while(True):
    response = requests.get(link + str(i), auth = ("Falconkira", "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"))
    temp = response.json()
    if len(temp) == 0:
        break
    i += 1
    print(i)
    repos.append(temp)

li = []
for i in repos:
    for j in i:
        li.append(j)

repos_len = len(li)
x = col.insert_many(li)

stars = col.find().sort("stargazers_count")

stars_list = []
for star in stars:
    stars_list.append(star["stargazers_count"])

max_s = stars_list[-1]
min_s = stars_list[0]
mean_s = np.mean(stars_list)
std_s = np.std(stars_list)
print("highest num of stargazers: ", max_s)
print("lowest num of stargazers: ", min_s)
print("average num of stargazers: ", mean_s)
print("standard deviation of stargazers: ", std_s)

percent_s = []
index_list = []
for i in [5,10,25,75,90,95]:
    index = int(len(stars_list)*i*0.01)
    tmp = stars_list[index]
    index_list.append(index)
    percent_s.append(tmp)
    print(str(i) + " percentiles of the distribution: ", tmp)

import matplotlib.pyplot as plt
plt.figure(figsize=(20,8),dpi=80)
plt.hist(stars_list, bins = 10)
plt.title("Distribution_Hist")
plt.xlabel("Values")
plt.ylabel("Count")
plt.show()
plt.savefig('distribution_fig.jpg')


def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2



def boxplot(q1,q3,i1,i3):
    fig, ax = plt.subplots()
    boxes = [
        {
            'label' : "stargazers",
            'whislo': min_s,    # Bottom whisker position
            'q1'    : q1,    # First quartile (25th percentile)
            'med'   : get_median(stars_list),    # Median         (50th percentile)
            'q3'    : q3,    # Third quartile (75th percentile)
            'whishi': max_s,    # Top whisker position
            'fliers': []        # Outliers
        }
    ]
    ax.bxp(boxes, showfliers=False)
    ax.set_ylabel("stars")
    plt.savefig("boxplot.png")

boxplot(percent_s[0],percent_s[-1],index_list[0],index_list[-1])
boxplot(percent_s[1],percent_s[-2],index_list[1],index_list[-2])
boxplot(percent_s[2],percent_s[-3],index_list[2],index_list[-3])

dic = {
"task-1-submission": {
"mean": mean_s,
"std": std_s,
"min": min_s,
"max": max_s,
"percentile_5": percent_s[0],
"percentile_10": percent_s[1],
"percentile_25": percent_s[2],
"percentile_75": percent_s[3],
"percentile_90": percent_s[4],
"percentile_95": percent_s[5]
}
}

db = client.hackacthon
col_answer = db.answer
x = col.insert_one(dic)