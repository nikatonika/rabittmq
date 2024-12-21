import pika
import numpy as np
import json
import time
from datetime import datetime
from sklearn.datasets import load_diabetes
 

while True:
    try:
        # добавляем время к сообщению
        message_id = datetime.timestamp(datetime.now())
        #Загрузка датасета
        X, y = load_diabetes(return_X_y=True)
        # Формируем случайный индекс
        random_row = np.random.randint(0, X.shape[0]-1)
 
        # подключение к очедери (rabitmq)
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
 
        # Создаём очереди
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')
        
        message_y_true = {
	        'id': message_id,
    	    'body': y[random_row]
	    }
        # Публикуем сообщения в очереди y_true и features
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
        print('[OK] ========> Cообщение с правильным ответом оправлено в очередь')
 
        message_features = {
	        'id': message_id,
    	    'body': list(X[random_row])
	    }

        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
        print('[OK] ========> Сообщение с вектором признаков отправлено в очередь')
 
        # Закрываем коннект
        connection.close()
	
    except:
        print('[FATAL] ========> Не удалось подключиться к очереди')

    time.sleep(10)
