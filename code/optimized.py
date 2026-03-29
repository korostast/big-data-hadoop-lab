import time
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType
from pyspark.sql.functions import col, round
from utils import log_executor_memory, logger


def main():
    logger.info(f"--- Optimized ---")
    
    spark = SparkSession.builder \
        .appName("Academic_Experiment_Optimized") \
        .master("spark://spark-master:7077") \
        .config("spark.sql.shuffle.partitions", "12") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    start_time = time.time()

    # 1. Read data with data schema to optimize further reading
    schema = StructType([
        StructField("VendorID", IntegerType(), True),
        StructField("tpep_pickup_datetime", StringType(), True),
        StructField("tpep_dropoff_datetime", StringType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("pickup_longitude", DoubleType(), True),
        StructField("pickup_latitude", DoubleType(), True),
        StructField("RateCodeID", IntegerType(), True),
        StructField("store_and_fwd_flag", StringType(), True),
        StructField("dropoff_longitude", DoubleType(), True),
        StructField("dropoff_latitude", DoubleType(), True),
        StructField("payment_type", IntegerType(), True),
        StructField("fare_amount", DoubleType(), True),
        StructField("extra", DoubleType(), True),
        StructField("mta_tax", DoubleType(), True),
        StructField("tip_amount", DoubleType(), True),
        StructField("tolls_amount", DoubleType(), True),
        StructField("improvement_surcharge", DoubleType(), True),
        StructField("total_amount", DoubleType(), True)
    ])

    hdfs_path = "hdfs://namenode:9000/data/dataset.csv"
    logger.info("Stage 1: read data (with known data schema)")
    t0 = time.time()
    df = spark.read.csv(hdfs_path, header=True, schema=schema)
    t1 = time.time()

    # 2. Optimizations
    logger.info("Stage 2: .repartition() + .cache()")
    optimized_df = df.repartition(12).cache()
    
    logger.info("Action: count() to initialize cache in memory")
    t0 = time.time()
    row_count = optimized_df.count()
    log_executor_memory(spark, stage_name="After .cache() и count()")
    logger.info(f"Read {row_count} rows. Time (with cache): {time.time() - t0:.2f} s.")

    # 3. Transform with cached data 
    logger.info("Stage 3: filtration and aggregation (using cache)")
    
    categorical_column = "VendorID"
    numeric_column = "trip_distance"

    # Actions:
    # 1. Filter not-null and negative values
    # 2. Group by vendor
    # 3. Count number of trips
    # 4. Compute average trip distance
    aggregated_df = optimized_df.filter((col(numeric_column).isNotNull()) & (col(numeric_column) > 0)) \
                                .groupBy(categorical_column) \
                                .agg(
                                    {"*": "count", numeric_column: "avg"}
                                ) \
                                .withColumnRenamed(f"avg({numeric_column})", "avg_distance") \
                                .withColumn("avg_distance", round(col("avg_distance"), 2)) \
                                .orderBy("count(1)", ascending=False)

    # 5. Force action
    logger.info("Action: show() for aggregation (Shuffle)")
    t1 = time.time()
    aggregated_df.show(10)
    log_executor_memory(spark, stage_name="After aggregation")
    logger.info(f"Aggregation completed. Time: {time.time() - t1:.2f} s.")

    total_time = time.time() - start_time
    logger.info(f"Total execution time: {total_time:.2f} s.")

    optimized_df.unpersist()
    spark.stop()

if __name__ == "__main__":
    main()