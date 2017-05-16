from flask import Flask, jsonify
from flask_restful import Resource, Api
import json

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"Greeting": "Hello World"})

@app.route("/staff_search/<string:name>", methods=['GET'])
def get_staff(name):
    name = name.lower()
    with open("staff_data.json", 'rb') as f:
        data = json.load(f)
    staff_names = data.keys()
    search_results = []
    for staff_name in staff_names:
        search_name = staff_name.encode('ascii', 'ignore').lower()
        if name in search_name:
            search_results.append(data[staff_name])
    if len(search_results) == 0:
        return jsonify({"Error": "No Academics Found."})
    else:
        return jsonify({"Staff": search_results})

if __name__ == "__main__":
    app.run()