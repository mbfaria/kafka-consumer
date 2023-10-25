docker run --net=host -i -t confluentinc/cp-schema-registry:latest kafka-avro-console-consumer \
--bootstrap-server localhost:9094 \
--property schema.registry.url=http://0.0.0.0:8081 \
--topic tb_order \
--property print.value=true \
--value-deserializer io.confluent.kafka.serializers.KafkaAvroDeserializer 
--from-beginning