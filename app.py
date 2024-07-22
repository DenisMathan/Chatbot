from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS, cross_origin

import threading
# from alfred import getBot 
from Perception import Perception
from Chatbot import Chatbot


app = Flask(__name__)
alfred = Chatbot({"max_tokens": 512})
perception = Perception()
csrf = CSRFProtect(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8081/", 'Access-Control-Allow-Origin': '*'}})
lock = threading.Lock()

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


# if __name__ == '__main__':
#     alfred = Chatbot({"max_tokens": 512})
#     print('test')
#     perception = Perception()
#     # app.run()
#     # app.run(debug=True,  ssl_context='adhoc')
#     app.run(debug = True, host="::", port=3333)