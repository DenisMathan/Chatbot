from flask import request, jsonify
from flask_cors import cross_origin
from app import app, csrf, alfred, perception, lock

@app.route('/')
@cross_origin()
def hello_world():
    return jsonify('Hello, World!')

@app.route('/api/chat', methods=['POST'])
@cross_origin()
@csrf.exempt
def chat():
    with lock:
        print('jippie!')
        question = request.get_json()['question']
        print(question)
        return jsonify(alfred.answer(question))

@app.route('/api/updateChroma', methods=['GET'])
def updateChroma():
    print('update')
    perception.setup()
    return jsonify('update successfull')