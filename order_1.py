import json
import pprint

path = "./workflow.json"

f = open(path)
data = json.load(f)

out_dict = {}
out_path = "./order.json"

for process in data.get("processes"):
    for i in process.get("ins"):
        if i in out_dict:
            out_dict[i] = out_dict[i] + process.get("outs")
        else:
            out_dict[i] = process.get("outs")

pp = pprint.PrettyPrinter(indent=4)

def get_name(item):
    return item.get("name")

signal_list = data.get("signals")
signal_list = list(map(get_name, signal_list))
#print(signal_list)
files= len(signal_list)
#print(files)
MAX = -1

distance_dict = {}

for i in range(files):
    distance_dict[signal_list[i]] = {}
    for j in range(files):
        distance_dict[signal_list[i]][signal_list[j]] = -1

def process_node(origin, file, distance):
    if distance_dict[signal_list[origin]][signal_list[file]] == -1 or distance_dict[signal_list[origin]][signal_list[file]] > distance:
        distance_dict[signal_list[origin]][signal_list[file]] = distance
    if file in out_dict:
        for out in out_dict[file]:
            process_node(origin, out, distance+1)

for i in range(files):
    process_node(i, i, 0)

# pp.pprint(distance_dict[11])

with open(out_path, 'w+') as f:
    json.dump(distance_dict, f, indent=2)
