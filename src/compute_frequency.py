import json
import math
import sys
import pandas as pd

with open('word_counts_more.json', 'r') as f:
    t = json.load(f)
    pass

output = {}
num_words = 10
for topic in t.keys():
    topic_tf_idfs = {}
    for word in t[topic]:
        total_use = 0
        for topic_ in t.keys():
            if word in t[topic_]:
                total_use += 1
                pass
            pass
        topic_tf_idfs[word] = t[topic][word] * math.log(1000 / total_use)
        pass
    output[topic] = sorted(topic_tf_idfs.items(), key=lambda x: x[1], reverse=True)
    output[topic] = [item[0] for item in output[topic]]
    if num_words < len(output[topic]):
        output[topic] = output[topic][:num_words]
        pass
    pass

with open('topic_characterization_more_10.json', 'w') as f:
    json.dump(output, f)
    pass
