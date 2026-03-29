FILENAME=$(basename "$1")
FILEPATH="/tmp/$FILENAME"
docker cp code/utils.py spark-master:/tmp

docker exec -it spark-master python3 -m pip show "requests" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "requests is installed already"
else
    echo "requests is not installed. Installing..."
    docker exec -it spark-master pip install requests
    
    if [ $? -eq 0 ]; then
        echo "requests is installed"
    else
        echo "requests installation failed. Abort"
        exit 1
    fi
fi


docker cp $1 spark-master:$FILEPATH
docker exec -it spark-master spark-submit --master spark://spark-master:7077 $FILEPATH
