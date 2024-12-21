import pika
import json
import os

# путь к файлу логирования
log_file = "./logs/metric_log.csv"

# создаём файл логирования, если он не существует, и записываем заголовок
if not os.path.exists(log_file):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "w") as f:
        f.write("id,y_true,y_pred,absolute_error\n")

# временное хранилище для данных
buffer = {}

# функция для обновления логов
def update_log(data_type, data):
    global buffer

    # получаем id и значение
    msg_id = data["id"]
    value = data["body"]

    if msg_id not in buffer:
        buffer[msg_id] = {"y_true": None, "y_pred": None}

    # обновляем буфер
    buffer[msg_id][data_type] = value

    # если в буфере есть обе метки, вычисляем абсолютную ошибку
    if buffer[msg_id]["y_true"] is not None and buffer[msg_id]["y_pred"] is not None:
        y_true = buffer[msg_id]["y_true"]
        y_pred = buffer[msg_id]["y_pred"]
        absolute_error = abs(y_true - y_pred)

        # записываем в лог
        with open(log_file, "a") as f:
            f.write(f"{msg_id},{y_true},{y_pred},{absolute_error}\n")

        # удаляем данные из буфера
        del buffer[msg_id]

# создаём функцию callback для обработки данных из очереди
def callback(ch, method, properties, body):
    try:
        print(f'Из очереди {method.routing_key} получено значение {json.loads(body)}')
        data = json.loads(body)
        if method.routing_key == "y_true":
            update_log("y_true", data)
        elif method.routing_key == "y_pred":
            update_log("y_pred", data)
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")

try:
    # создаём подключение к серверу RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # объявляем очередь y_true
    channel.queue_declare(queue='y_true')
    # объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')

    # извлекаем сообщения из очередей
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )

    # запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()

except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')
