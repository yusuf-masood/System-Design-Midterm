from kafka import KafkaProducer
import json

KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

order_id = 1
amount = 500  # Change this value to test failure (e.g., 2000)

print(f"Sending checkout event for order {order_id}")
producer.send('checkout_events', {'order_id': order_id, 'amount': amount})
