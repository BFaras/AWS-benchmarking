from flask import Flask
import requests
import json


app = Flask(__name__)

@app.route('/')
def my_app():
    return 'Minimal flask app made by the greatest alive... momomomomomo'

@app.route('/cluster1')
def cluster1():
    headers = {"content-type": "application/json"}
    return requests.get("http://169.254.169.254/latest/meta-data/instance-id",headers).content

@app.route('/cluster2')
def cluster2():
    headers = {"content-type": "application/json"}
    return requests.get("http://169.254.169.254/latest/meta-data/instance-id",headers).content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

