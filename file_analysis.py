import json
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import pprint

config = yaml.safe_load(open("./config.yml"))

pp = pprint.PrettyPrinter(indent=2, width=1)

path = './file_size.json'
path_freq = './freq.json'

#1

plot1 = plt.figure(1)
ax = plt.subplot(111)

with open(path) as f:
    data = json.load(f)

file_size = []
for key in data:
    file_size.append(data[key])

num_bins = 50
ax.hist(file_size, num_bins, log=True)

plt.xlabel('File Size [B]')
plt.ylabel('Number of files')

plt.title('File size distribution in %s workflow' % config['simulator']['name'])
plt.savefig('sizes.png')

#2

with open(path_freq) as f:
    data = json.load(f)

file_freq = {}
for key in data:
    if data[key] not in file_freq:
        file_freq[data[key]] = 1
    else:
        file_freq[data[key]] += 1


pp.pprint(file_freq)

plt.show()
