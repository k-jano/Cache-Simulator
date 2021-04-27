import json
import redis

from flask import Flask, request
app = Flask(__name__)

@app.route('/process', methods=["POST"])
def process():
    body = request.json
    print('Process job %s' % body)
    return 'Processed'



if __name__ == "__main__":
    wf_key = 1
    keys = []

    r = redis.StrictRedis(host="localhost", port=6379, db=0)
    for key in r.scan_iter("wf:" + str(wf_key) + ":task:[0-9]*:*"):
        print(key)
        keys.append(key)

    

    # for key in keys:
    #     r.zrange(key, 0, -1)
    
