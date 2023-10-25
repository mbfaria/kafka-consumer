from datetime import datetime
from confluent_kafka import Producer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import random

schema_registry_url = "http://localhost:8081"
schema_registry_subject = "tb_order"
schema = """
    {
        "type": "record", 
        "name": "Event", 
        "fields": [
            {
                "name": "id_order", 
                "type": "string"
            }, 
            {
                "name": "id_customer", 
                "type": "string"
            }, 
            {
                "name": "vl_price", 
                "type": "double"
            },
            {
                "name": "ts_event", 
                "type": {"type": "long", "logicalType": "timestamp-millis"}
            }
        ]
    }
    """


kafka_broker = "localhost:9094"
kafka_topic = "tb_order"


schema_registry_conf = {"url": schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
schema_registry_client.set_compatibility(level="NONE")

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client, schema_str=schema
)

producer_conf = {"bootstrap.servers": kafka_broker}

producer = Producer(producer_conf)

for i in range(100):
    event = {
        "id_order": f"{random.randint(1, 1000)}".zfill(10),
        "id_customer": f"{random.randint(1, 1000)}".zfill(5),
        "vl_price": round(random.uniform(0, 1000), 2),
        "ts_event": datetime.now(),
    }
    producer.produce(
        topic=kafka_topic,
        value=avro_serializer(
            event, SerializationContext(kafka_topic, MessageField.VALUE)
        ),
    )

    producer.flush()
