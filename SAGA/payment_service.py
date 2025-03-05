from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'payment_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    order_id = data['order_id']

    if data['status'] == 'PAYMENT_ROLLBACK':
        print(f"[Payment] Rolling back payment for order {order_id}")
    else:
        print(f"[Payment] Processing payment for order {order_id}")
        success = data['amount'] < 1000  # Simulate failure if amount > 1000
        producer.send('payment_events', {'order_id': order_id, 'status': 'PAYMENT_SUCCESS' if success else 'PAYMENT_FAILED'})
