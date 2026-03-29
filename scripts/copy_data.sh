docker cp $1 namenode:/tmp/dataset.csv
docker exec -it namenode hdfs dfs -mkdir -p /data
docker exec -it namenode hdfs dfs -D dfs.blocksize=134217728 -put /tmp/dataset.csv /data/
docker exec -it namenode hdfs dfs -ls /data/
docker exec -it namenode hdfs fsck /data/dataset.csv -files -blocks -locations