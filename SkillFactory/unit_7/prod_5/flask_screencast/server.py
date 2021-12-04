import numpy as np
import pickle
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

with open('hw1.pkl', 'rb') as pkl_file:
    model = pickle.load(pkl_file)


@app.route('/hello')
def hello_func():
    name = request.args.get('name')
    return f'hello {name}!'


@app.route('/time')
def current_time():
    return {'time': datetime.now()}


@app.route('/add', methods=['POST'])
def add():
    num = request.json.get('num')
    if num > 10:
        return 'too much', 400
    return jsonify({'result': num + 1})


@app.route('/predict', methods=['POST'])
def predict():
    numbers = request.json.get('numbers')
    print(numbers)
    result = model.predict(np.array(numbers).reshape(1, -1))
    return jsonify({'prediction': result[0]})


if __name__ == '__main__':
    app.run('localhost', 5000)
