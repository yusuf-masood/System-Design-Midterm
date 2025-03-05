from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'inventory_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    order_id = data['order_id']

    if data['status'] == 'ROLLBACK_STOCK':
        print(f"[Inventory] Rolling back stock for order {order_id}")
    else:
        print(f"[Inventory] Reserving stock for order {order_id}")
        success = True  # Simulate inventory always succeeds
        producer.send('inventory_events', {'order_id': order_id, 'status': 'STOCK_RESERVED' if success else 'STOCK_FAILED'})
