from pathlib import Path
import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round
from utils import log_executor_memory, logger


def main():
    logger.info(f"--- Baseline ---")
    
    spark = SparkSession.builder \
        .appName("Academic_Experiment_Baseline") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    start_time = time.time()

    # 1. Read data
    hdfs_path = "hdfs://namenode:9000/data/dataset.csv"
    logger.info("Stage 1: read data from HDFS")
    
    # inferSchema=True forcefully create 1 job for types detection
    # From documentation: "Infers the input schema automatically from data. It requires one extra pass over the data"
    # https://spark.apache.org/docs/latest/sql-data-sources-csv.html#:~:text=read/write-,inferSchema,-false
    df = spark.read.csv(hdfs_path, header=True, inferSchema=True)
    
    # Force Action for measuring data reading into memory
    logger.info("Run count()")
    t0 = time.time()
    row_count = df.count()
    log_executor_memory(spark, stage_name="After .count()")
    logger.info(f"Read {row_count} rows. Time: {time.time() - t0:.2f} s.")

    # 2. Transform
    logger.info("Stage 2: filtration and aggregation")
    categorical_column = "VendorID"
    numeric_column = "trip_distance"
    
    # Actions:
    # 1. Filter not-null and negative values
    # 2. Group by vendor
    # 3. Count number of trips
    # 4. Compute average trip distance
    aggregated_df = df.filter((col(numeric_column).isNotNull()) & (col(numeric_column) > 0)) \
                      .groupBy(categorical_column) \
                      .agg(
                          {"*": "count", numeric_column: "avg"}
                      ) \
                      .withColumnRenamed(f"avg({numeric_column})", "avg_distance") \
                      .withColumn("avg_distance", round(col("avg_distance"), 2)) \
                      .orderBy("count(1)", ascending=False)

    # 3. Force action
    logger.info("Action: show() for aggregation (Shuffle)")
    t1 = time.time()
    aggregated_df.show(10)
    log_executor_memory(spark, stage_name="After aggregation")
    logger.info(f"Aggregation completed. Time: {time.time() - t1:.2f} s.")

    total_time = time.time() - start_time
    logger.info(f"Total execution time: {total_time:.2f} s.")

    spark.stop()

if __name__ == "__main__":
    main()
