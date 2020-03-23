from flask import Flask, request, jsonify
from dbaccess import FireStoreAccess

app = Flask(__name__)
db_acc = FireStoreAccess()

@app.route("/auth_db", methods=['POST'])
def auth_db():
    data = request.json
    model_key = data.get("model_key")
    password = data.get("password")
    username = db_acc.auth_db(model_key, password)
    ok = False if username is None else True
    response = {"ok" : ok}
    if ok:
        response['username'] = username
    return jsonify(response)


@app.route("/auth_amqp", methods=['POST'])
def auth_amqp():
    data = request.json
    model_key = data.get("model_key")
    password = data.get("password")
    amqp_url = db_acc.auth_amqp(model_key, password)
    ok = False if amqp_url is None else True
    response = {'ok' : ok}
    if ok:
        response["amqp_url"] = amqp_url
    return jsonify(response)


@app.route("/start_training", methods=['POST'])
def start_training():
    data = request.json
    model_key = data.get("model_key")
    username = data.get("username")
    JSON = data.get("JSON")
    return jsonify({
        "new_training_id" : db_acc.start_training(model_key, username, JSON)
    })

@app.route("/end_training", methods=['POST'])
def end_training():
    data = request.json
    model_key = data.get("model_key")
    username = data.get("username")
    training_id = data.get("training_id")
    db_acc.end_training(model_key, username, training_id)
    return "", 200

@app.route("/epoch_begin", methods=['POST'])
def epoch_begin():
    data = request.json
    model_key = data.get("model_key")
    username = data.get("username")
    JSON = data.get("JSON")
    db_acc.epoch_begin(model_key, username, JSON)
    return "", 200

@app.route("/epoch_end", methods=['POST'])
def epoch_end():
    data = request.json
    model_key = data.get("model_key")
    username = data.get("username")
    JSON = data.get("JSON")
    db_acc.epoch_end(model_key, username, JSON)
    return "", 200

if __name__ == "__main__":
    app.run(debug=True)
