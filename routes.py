
@app.route('/')
@cross_origin()
def hello_world():
    return jsonify('Hello, World!')