import json

from flask import Flask, request
app = Flask(__name__)

@app.route('/process', methods=["POST"])
def process():
    body = request.json
    print('Process job %s' % body)
    return 'Processed'

if __name__ == "__main__":
    app.run()
