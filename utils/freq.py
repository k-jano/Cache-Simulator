import json
import pprint

path = "./Montagewf.json"

#f = open(path)
with open(path) as f:
    data = json.load(f)

pp = pprint.PrettyPrinter(indent=4)

frequency_dict = {}

def get_name(item):
    return item.get("name")

signal_list = data.get("signals")
signal_list = list(map(get_name, signal_list))

#print(signal_list)

for i in range(len(signal_list)):
    frequency_dict[signal_list[i]] = 0

#pp.pprint(frequency_dict)

process_list = data.get("processes")

for process in process_list:
    for file in process.get("ins"):
        frequency_dict[signal_list[file]] +=1

#pp.pprint(frequency_dict)

out_path = "./freq.json"

with open(out_path, 'w+') as f:
    json.dump(frequency_dict, f, indent=2)
