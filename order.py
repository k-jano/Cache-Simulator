import json
import pprint

path = "./workflow.json"

f = open(path)
data = json.load(f)

out_dict = {}

for process in data.get("processes"):
    for i in process.get("ins"):
        if i in out_dict:
            out_dict[i] = out_dict[i] + process.get("outs")
        else:
            out_dict[i] = process.get("outs")

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(out_dict)

files= 906
MAX = -1

distance_dict = {}

for i in range(files):
    distance_dict[i] = {}
    for j in range(files):
        distance_dict[i][j] = -1

def process_node(origin, file, distance):
    if distance_dict[origin][file] == -1 or distance_dict[origin][file] > distance:
        distance_dict[origin][file] = distance
    if file in out_dict:
        for out in out_dict[file]:
            process_node(origin, out, distance+1)

for i in range(files):
    process_node(i, i, 0)

pp.pprint(distance_dict[11])
