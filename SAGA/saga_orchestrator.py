from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_SERVER = 'localhost:9092'

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka consumer setup
checkout_consumer = KafkaConsumer(
    'checkout_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

payment_consumer = KafkaConsumer(
    'payment_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

inventory_consumer = KafkaConsumer(
    'inventory_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

shipping_consumer = KafkaConsumer(
    'shipping_events',
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def handle_checkout_events():
    for message in checkout_consumer:
        data = message.value
        order_id = data['order_id']
        print(f"[Saga] Received checkout event for order {order_id}. Starting payment step.")
        producer.send('payment_events', {'order_id': order_id, 'amount': data['amount']})

def handle_payment_events():
    for message in payment_consumer:
        data = message.value
        order_id = data['order_id']

        if data['status'] == 'PAYMENT_SUCCESS':
            print(f"[Saga] Payment successful for order {order_id}, proceeding to Inventory")
            producer.send('inventory_events', {'order_id': order_id, 'status': 'RESERVE_STOCK'})
        else:
            print(f"[Saga] Payment failed for order {order_id}, cancelling order.")
            producer.send('checkout_events', {'order_id': order_id, 'status': 'ORDER_FAILED'})

def handle_inventory_events():
    for message in inventory_consumer:
        data = message.value
        order_id = data['order_id']

        if data['status'] == 'STOCK_RESERVED':
            print(f"[Saga] Stock reserved for order {order_id}, proceeding to Shipping")
            producer.send('shipping_events', {'order_id': order_id, 'status': 'SHIP_ORDER'})
        else:
            print(f"[Saga] Inventory failed for order {order_id}, rolling back Payment.")
            producer.send('payment_events', {'order_id': order_id, 'status': 'PAYMENT_ROLLBACK'})

def handle_shipping_events():
    for message in shipping_consumer:
        data = message.value
        order_id = data['order_id']

        if data['status'] == 'SHIPPING_SUCCESS':
            print(f"[Saga] Order {order_id} successfully shipped!")
        else:
            print(f"[Saga] Shipping failed for order {order_id}, rolling back Inventory and Payment.")
            producer.send('inventory_events', {'order_id': order_id, 'status': 'ROLLBACK_STOCK'})
            producer.send('payment_events', {'order_id': order_id, 'status': 'PAYMENT_ROLLBACK'})

# Start listening to events
print("[Saga] Orchestrator is running...")
handle_checkout_events()
