from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    BooleanType,
    TimestampType,
)
import os

schema = StructType(
    [
        StructField("database", StringType(), True),
        StructField("domain", StringType(), True),
        StructField("stream", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("page_title", StringType(), True),
        StructField("user_text", StringType(), True),
        StructField("user_is_bot", BooleanType(), True),
        StructField("comment", BooleanType(), True),
    ]
)

spark = (
    SparkSession.builder.master("local[2]").appName("SensorDataStreaming").getOrCreate()
)

socketDF = (
    spark.readStream.format("socket")
    .option("host", "localhost")
    .option("port", 9999)
    .load()
)

# data is in json format
parsed_df = socketDF.select(from_json(col("value"), schema).alias("data")).select(
    "data.*"
)

# saving the data to file in append mode, csv format
directory = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(directory, "output")
checkpoint_path = os.path.join(directory, "checkpoint")

query = (
    parsed_df.writeStream.outputMode("append")
    .format("csv")
    .option("path", output_path)
    .option("checkpointLocation", checkpoint_path)
    .start()
)

query.awaitTermination()
