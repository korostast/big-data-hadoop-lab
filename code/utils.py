import logging

import requests


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def log_executor_memory(spark_session, stage_name=""):
    app_id = spark_session.sparkContext.applicationId
    api_url = f"http://localhost:4040/api/v1/applications/{app_id}/executors"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        executors_data = response.json()
        total_used_mb = 0
        for exc in executors_data:
            if exc['id'] != 'driver':
                exc_id = exc['id']
                host = exc['hostPort'].split(':')[0]
                
                max_mem_mb = exc['maxMemory'] / (1024 * 1024)
                used_mem_mb = exc['memoryUsed'] / (1024 * 1024) # Storage Memory (Cache)
                total_used_mb += used_mem_mb
                
                logger.info(f"Worker [{exc_id} | {host}]: Cache Used = {used_mem_mb:.2f} MB / Max = {max_mem_mb:.2f} MB")
                
        logger.info(f"Total amount of cached data in cluster: {total_used_mb:.2f} MB")
        
    except Exception as e:
        logger.exception(f"Cannot get memory data of executors: {e}")