import pika
import pickle
import numpy as np
import json
 
# читаем файл с нашей моделью
with open('model.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)
 
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
 
    # Создаем очереди y_pred и features
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')
 
    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        print(f'[OK] =======> Получено сообщение с  вектор признаков {body}')
        message = json.loads(body)
        message_id = message['id']
        features = message['body']
        pred = regressor.predict(np.array(features).reshape(1, -1))
        message_y_pred = {
	        'id': message_id,
    	    'body': pred[0]
	    }
        channel.basic_publish(exchange='',
                        routing_key='y_pred',
                        body=json.dumps(message_y_pred))
        print(f'[OK] =======> Предсказание {pred[0]} отправлено в очередь y_pred')
 
    # Извлекаем сообщение из очереди features
    # on_message_callback показывает, какую функцию вызвать при получении сообщения
    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('[OK] =======> ...Ожидание сообщений, для выхода нажмите CTRL+C')
 
    # Запускаем в режим приема сообщений
    channel.start_consuming()
except:
    print('[FATAL] ========> Не удалось подключиться к очереди')
