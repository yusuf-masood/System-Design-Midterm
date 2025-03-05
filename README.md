# System-Design-Midterm

# 🛒 E-Commerce Checkout Workflow using Kafka & Saga Pattern

## 📌 Overview
This project implements a **Saga Pattern** within a **single microservice** architecture for an **e-commerce checkout workflow**. It ensures **event-driven coordination** using Apache Kafka, handling **Payment, Inventory, and Shipping** services.

If any step fails, previous steps are **compensated** in **reverse order**, ensuring data consistency.

---

## 🏗️ Architecture

The system consists of:
- **Kafka Topics**:
  - `checkout_events` → Trigger checkout process
  - `payment_events` → Handles payment processing
  - `inventory_events` → Manages inventory stock
  - `shipping_events` → Handles shipping updates

- **Microservices** (Written in Python):
  - `payment_service.py`
  - `inventory_service.py`
  - `shipping_service.py`
  - `send_checkout_event.py` (Triggers a new order)

Each service **subscribes to its respective Kafka topic** and **produces compensating events** in case of failure.

---

## 🚀 Setup Instructions

### **1️⃣ Prerequisites**
Ensure you have installed:
- **Python 3.8+**
- **Apache Kafka & Zookeeper**
- Required Python libraries:
  ```sh
  pip install kafka-python
  ```

---

### **2️⃣ Start Kafka & Zookeeper**
In a new terminal, start **Zookeeper**:
```sh
cd C:\kafka_2.13-3.9.0\bin\windows
.\zookeeper-server-start.bat ..\..\config\zookeeper.properties
```
In another terminal, start **Kafka**:
```sh
cd C:\kafka_2.13-3.9.0\bin\windows
.\kafka-server-start.bat ..\..\config\server.properties
```

---

### **3️⃣ Create Kafka Topics**
Run the following commands to create required Kafka topics:

```sh
cd C:\kafka_2.13-3.9.0\bin\windows

.\kafka-topics.bat --create --topic checkout_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
.\kafka-topics.bat --create --topic payment_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
.\kafka-topics.bat --create --topic inventory_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
.\kafka-topics.bat --create --topic shipping_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Verify topics:
```sh
.\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Expected Output:
```
checkout_events
payment_events
inventory_events
shipping_events
```

---

### **4️⃣ Run Microservices**
Start each microservice **in a separate terminal**:

```sh
python payment_service.py
python inventory_service.py
python shipping_service.py
```

---

### **5️⃣ Trigger Checkout**
Send a test order event:
```sh
python send_checkout_event.py
```

Expected output:
```
Sending checkout event for order 1
```

---

### **6️⃣ Monitor Kafka Events**
To verify event flow, you can run the following **Kafka consumers**:

```sh
.\kafka-console-consumer.bat --topic checkout_events --bootstrap-server localhost:9092 --from-beginning
.\kafka-console-consumer.bat --topic payment_events --bootstrap-server localhost:9092 --from-beginning
.\kafka-console-consumer.bat --topic inventory_events --bootstrap-server localhost:9092 --from-beginning
.\kafka-console-consumer.bat --topic shipping_events --bootstrap-server localhost:9092 --from-beginning
```

You should see events flowing between services.

---

### **7️⃣ How Saga Pattern Works Here**
1. **Checkout Event**
   - Triggers an order processing event.
2. **Payment Service**
   - Deducts the amount.
   - If **payment fails**, it **triggers a compensation event**.
3. **Inventory Service**
   - Reserves stock.
   - If **inventory is insufficient**, it **triggers a rollback event**.
4. **Shipping Service**
   - Ships the order.
   - If **shipping fails**, it **triggers a rollback event**.

If any service **fails**, the previous services **undo their actions**, ensuring consistency.

---

## 📜 **Project Files**
| File | Description |
|------|------------|
| `payment_service.py` | Handles payments, listens on `checkout_events` |
| `inventory_service.py` | Manages inventory, listens on `payment_events` |
| `shipping_service.py` | Manages shipping, listens on `inventory_events` |
| `send_checkout_event.py` | Sends a test order event |

---

## 🏁 Conclusion
- This project **ensures data consistency** across microservices using the **Saga Pattern**.
- Apache Kafka acts as the **event broker**, ensuring reliable event-driven coordination.
- Each service operates **independently** while reacting to Kafka events.

---

## 📌 Future Improvements
- Add **database storage** for order tracking.
- Add **Kafka Streams** for real-time monitoring.

---

## 📝 **Author**
- **Sayed Yusuf Masood**
- **GitHub:** (https://github.com/yusuf-masood/System-Design-Midterm)
