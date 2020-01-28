from flask import Flask, request, Response, jsonify

app = Flask(__name__)

def validate_key(key):
    return key == "varun"

@app.route("/auth", methods=['POST'])
def auth():
    print(request.json)
    json = request.json
    if validate_key(json['model_key']):
        return "", 200
    return "", 401

@app.route("/start", methods=['POST'])
def start():
    print("training_start:", request.json)
    resp = {'training_id' : 2001}
    return jsonify(resp)

@app.route("/end", methods=['POST'])
def end():
    print("trainind_end:", request.json)
    return ""

@app.route("/epochbegin", methods=['POST'])
def epoch_begin():
    print("epoch_begin:", request.json)
    return ""

@app.route("/epochend", methods=['POST'])
def epoch_end():
    print("epoch_end:", request.json)
    return ""

app.run(debug=True)
