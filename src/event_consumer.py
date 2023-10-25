from pyspark.sql import SparkSession, SQLContext, DataFrame
from pyspark.sql.functions import col, substring, conv, hex, expr
from pyspark.sql.avro.functions import from_avro
from confluent_kafka.schema_registry import SchemaRegistryClient

packages = [
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
    "org.apache.spark:spark-avro_2.12:3.5.0",
]
spark = (
    SparkSession.builder.appName("KafkaConsumer")
    .config("spark.jars.packages", ",".join(packages))
    .config(
        "spark.jars",
        "./scala-code/target/scala-2.12/myscalaclass_2.12-2.0.jar",
    )
    .getOrCreate()
)

sc = spark.sparkContext
sc.setLogLevel("ERROR")
sqlContext = SQLContext(spark)


kafka_server = "localhost:9094"
kafka_topic = "tb_order"

kafka_options = {
    "kafka.bootstrap.servers": kafka_server,
    "subscribe": kafka_topic,
    "startingOffsets": "earliest",
}

schema_registry_url = "http://localhost:8081"
schema_registry_conf = {"url": schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)


def run_scala_function(df, column_name):
    ssqlContext = sqlContext._ssql_ctx
    scalaObject = sc._jvm.simple.MyScalaClass(ssqlContext, df._jdf)
    return DataFrame(scalaObject.myScalaFunction(column_name), ssqlContext)


def consumer(batch_df, _):
    batch_df = batch_df.withColumn(
        "schema_id", conv(hex(substring(col("value"), 2, 4)), 16, 10)
    )
    list_schema_ids = batch_df.select("schema_id").distinct().collect()

    result_df = None
    for schema_id in list_schema_ids:
        schema = schema_registry_client.get_version(
            f"{kafka_topic}-value", schema_id.schema_id
        )
        deserialized_df = batch_df.filter(
            col("schema_id") == schema_id.schema_id
        ).withColumn(
            "value", from_avro(expr("substring(value, 6)"), schema.schema.schema_str)
        )
        result_df = (
            result_df.unionByName(deserialized_df, allowMissingColumns=True)
            if result_df
            else deserialized_df
        )
    result_df = run_scala_function(result_df, "value.id_order")
    result_df = run_scala_function(result_df, "value.id_customer")
    result_df = run_scala_function(result_df, "topic")
    result_df.show(50, vertical=True, truncate=False)
    return result_df


df = spark.readStream.format("kafka").options(**kafka_options).load()

query = df.writeStream.foreachBatch(consumer).start().awaitTermination()

# query = df.writeStream.outputMode("append").format("console").start()

# query.awaitTermination()
