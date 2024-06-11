from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg
import pyspark.sql.functions as F
import os

spark = (
    SparkSession.builder.master("local[2]").appName("SensorDataStreaming").getOrCreate()
)

socketDF = (
    spark.readStream.format("socket")
    .option("host", "localhost")
    .option("port", 9999)
    .load()
)

# data is in string format
parsed_df = socketDF.selectExpr("split(value, ',') AS data")
parsed_dff = parsed_df.selectExpr(
    "CAST(data[0] AS INT) AS pond_id",
    "CAST(data[1] AS TIMESTAMP) AS created_at",
    "CAST(data[2] AS INT) AS entry_id",
    "CAST(data[3] AS FLOAT) AS temp_c",
    "CAST(data[4] AS INT) AS turbidity_ntu",
    "CAST(data[5] AS FLOAT) AS dissolved_oxygen_g_ml",
    "CAST(data[6] AS FLOAT) AS ph",
    "CAST(data[7] AS FLOAT) AS ammonia_g_ml",
    "CAST(data[8] AS FLOAT) AS nitrate_g_ml",
    "CAST(data[9] AS INT) AS population",
    "CAST(data[10] AS FLOAT) AS fish_length_cm",
    "CAST(data[11] AS FLOAT) AS fish_weight_g",
)

streaming_df = parsed_dff.withColumn(
    "created_at", F.to_timestamp("created_at", "yyyy-MMdd'T'HH:mm:ss")
)

windowed_df = (
    streaming_df.withWatermark("created_at", "15 seconds")
    .groupBy(window(col("created_at"), "30 seconds", "30 seconds"), col("pond_id"))
    .agg(
        avg("temp_c").alias("avg_temp_c"),
        avg("dissolved_oxygen_g_ml").alias("avg_dissolved_oxygen_g_ml"),
        avg("ph").alias("avg_ph"),
        avg("ammonia_g_ml").alias("avg_ammonia_g_ml"),
        avg("nitrate_g_ml").alias("avg_nitrate_g_ml"),
    )
)

selected_df = windowed_df.select(
    "window.start",
    "window.end",
    "pond_id",
    "avg_temp_c",
    "avg_dissolved_oxygen_g_ml",
    "avg_ph",
    "avg_ammonia_g_ml",
    "avg_nitrate_g_ml",
)

# saving the data to file in append mode, csv format
directory = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(directory, "output")
checkpoint_path = os.path.join(directory, "checkpoint")

query1 = (
    parsed_dff.writeStream.outputMode("append")
    .format("csv")
    .option("path", output_path)
    .option("checkpointLocation", checkpoint_path)
    .start()
)

query2 = (
    selected_df.writeStream.outputMode("complete")
    .format("console")
    .option("truncate", False)
    .start()
)

query1.awaitTermination()
query2.awaitTermination()
