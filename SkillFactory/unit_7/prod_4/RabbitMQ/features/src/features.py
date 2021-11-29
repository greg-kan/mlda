"""features.py"""
import pika
import json
import numpy as np
import time
from sklearn.datasets import load_diabetes
import signal


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


signal.signal(signal.SIGINT, signal_handler)

X, y = load_diabetes(return_X_y=True)

interrupted = False
while True:
    try:
        if interrupted:
            print("\nGotta go!")
            break

        random_row = np.random.randint(0, X.shape[0] - 1)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))  # host='localhost'
        channel = connection.channel()

        channel.queue_declare(queue='Features')
        channel.queue_declare(queue='y_true')

        channel.basic_publish(exchange='',
                              routing_key='Features',
                              body=json.dumps(list(X[random_row])))
        print(f'Сообщение с вектором признаков {list(X[random_row])} отправлено в очередь')

        channel.basic_publish(exchange='',
                              routing_key='y_true',
                              body=json.dumps(y[random_row]))

        print(f'Сообщение с правильным ответом {y[random_row]} отправлено в очередь')
        connection.close()
        time.sleep(3)
    except:
        print('Не удалось подключиться к очереди')
        break
