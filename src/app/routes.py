from flask import request, jsonify
from flask_cors import cross_origin
from app import app, csrf, alfred, perception, lock

from dotenv import load_dotenv
import os
root_path = os.getenv('ROOT_PATH', ".")
load_dotenv()

@app.route('/')
@cross_origin()
def hello_world():
    return jsonify('Hello, World!')

@app.route('/api/chat', methods=['POST'])
@cross_origin()
@csrf.exempt
def chat():
    with lock:
        question = request.get_json()['question']
        return jsonify(alfred.answer(question))

@app.route('/api/updateChroma', methods=['GET'])
def updateChroma():
    print('update')
    perception.setup()
    return jsonify('update successfull')

@app.route('/api/getKnowledge', methods=['GET'])
@cross_origin()
@csrf.exempt
def getKnowledge():
    knowledge = perception.getKnowledge()
    return knowledge

@app.route('/api/updateKnowledge', methods=['POST'])
@cross_origin()
@csrf.exempt
def updateKnowledge():
    try:
        pwToken = request.get_json()['pwToken']
    except:
        return "sorry you don't have accessrights" 
    token = os.getenv("CHROMA_UPDATE_TOKEN")
    if(pwToken != token):
        return "sorry you don't have accessrights!"
    knowledge = perception.updateKnowledge(request.get_json()['knowledge'])
    return knowledge