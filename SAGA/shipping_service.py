from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'shipping_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    order_id = data['order_id']

    print(f"[Shipping] Shipping order {order_id}")
    success = True  # Simulate shipping always succeeds
    producer.send('shipping_events', {'order_id': order_id, 'status': 'SHIPPING_SUCCESS' if success else 'SHIPPING_FAILED'})
