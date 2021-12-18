import matplotlib.pyplot as plt
import json
import numpy as np


with open('id_topic_sentiment_words.json', 'r') as f:
    itsw = json.load(f)
    pass

with open('topic_characterization_more_10.json', 'r') as f:
    tc = json.load(f)
    pass

topic_dist = {}
sentiment_dist = {}
topic_sent_dist = {}
for id in itsw.keys():
    topic = itsw[id]['topic']
    sentiment = itsw[id]['sentiment']
    if topic not in topic_dist:
        topic_dist[topic] = 1
        topic_sent_dist[topic] = {}
    else:
        topic_dist[topic] += 1
        pass
    if sentiment not in sentiment_dist:
        sentiment_dist[sentiment] = 1
    else:
        sentiment_dist[sentiment] += 1
        pass

    if sentiment not in topic_sent_dist[topic]:
        topic_sent_dist[topic][sentiment] = 1
    else:
        topic_sent_dist[topic][sentiment] += 1
    pass

for topic in topic_sent_dist:
    total = 0
    for sentiment in topic_sent_dist[topic]:
        total += topic_sent_dist[topic][sentiment]
    for sentiment in topic_sent_dist[topic]:
        topic_sent_dist[topic][sentiment] = topic_sent_dist[topic][sentiment]/total

negative_topic = []
neutral_topic = []
positive_topic = []
sum_negative_neutral_topic = []
topics_list = ['SV', 'VA', 'RE', 'PO', 'CU']

for topic in topics_list:
    negative_topic.append(topic_sent_dist[topic]['negative'])
    neutral_topic.append(topic_sent_dist[topic]['neutral'])
    positive_topic.append(topic_sent_dist[topic]['positive'])
    sum_negative_neutral_topic.append(topic_sent_dist[topic]['negative'] + topic_sent_dist[topic]['neutral'])


plt.pie(x=topic_dist.values(), labels=topic_dist.keys(), autopct='%1.2f%%')
plt.savefig('images/topic_distribution.png')
plt.show()

params = {
    'figure.figsize': '7, 6'
}
plt.rcParams.update(params)

for topic in topics_list:
    data = {}
    for word in tc[topic]:
        data[word] = {}
        for s in sentiment_dist.keys():
            data[word][s] = 0
            pass
        for id in itsw.keys():
            t = itsw[id]['topic']
            s = itsw[id]['sentiment']
            ws = itsw[id]['words']
            if word in ws and topic == t:
                data[word][s] += 1
                pass
            pass
        pass
    x_labels = tc[topic]
    x_labels.append('all tweets')
    ind = np.arange(len(x_labels))
    plt.xticks(ind, x_labels, rotation=30)
    plt.ylabel('proportion of sentiment')
    negative = []
    neutral = []
    positive = []
    sum_negative_neutral = []
    for word in data.keys():
        sum = data[word]['negative'] + data[word]['neutral'] + data[word]['positive']
        negative.append(data[word]['negative']/sum)
        neutral.append(data[word]['neutral']/sum)
        positive.append(data[word]['positive']/sum)
        sum_negative_neutral.append((data[word]['negative'] + data[word]['neutral'])/sum)
        pass
    negative.append(topic_sent_dist[topic]['negative'])
    neutral.append(topic_sent_dist[topic]['neutral'])
    positive.append(topic_sent_dist[topic]['positive'])
    sum_negative_neutral.append(topic_sent_dist[topic]['negative'] + topic_sent_dist[topic]['neutral'])

    p1 = plt.bar(ind, negative, 0.5, color='red')
    p2 = plt.bar(ind, neutral, 0.5, bottom=negative, color='green')
    p3 = plt.bar(ind, positive, 0.5, bottom=sum_negative_neutral, color='blue')
    plt.legend((p1[0], p2[0], p3[0]), ('negative', 'neutral', 'positive'))
    plt.savefig('images/'+topic+'_word_sentiment.png')
    plt.show()
    output = {}
    for i, word in enumerate(x_labels):
        if positive[i] == 0:
            output[word] = 'inf'
        else:
            output[word] = negative[i]/positive[i]
        pass
    with open('data/'+topic+'_word_sentiment.json', 'w') as f:
        json.dump(output, f)
        pass
    pass

x_labels = topics_list
ind = np.arange(len(topics_list))
plt.xticks(ind, x_labels)
plt.ylabel('proportion of sentiment')
p1 = plt.bar(ind, negative_topic, 0.5, color='red')
p2 = plt.bar(ind, neutral_topic, 0.5, bottom=negative_topic, color='green')
p3 = plt.bar(ind, positive_topic, 0.5, bottom=sum_negative_neutral_topic, color='blue')
plt.legend((p1[0], p2[0], p3[0]), ('negative', 'neutral', 'positive'))
plt.savefig('images/'+'topic_sentiment.png')
plt.show()

output = {}
for i, word in enumerate(x_labels):
    output[word] = {'negative': negative_topic[i], 'neutral': neutral_topic[i], 'positive': positive_topic[i]}
    pass
with open('data/'+'topic_sentiment.json', 'w') as f:
    json.dump(output, f)
    pass
