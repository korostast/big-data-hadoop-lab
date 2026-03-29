FILENAME=$(basename "$1")
FILEPATH="/tmp/$FILENAME"
docker cp $1 spark-master:$FILEPATH

docker exec -it spark-master python3 -m pip show "psutil" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "psutil is installed already"
else
    echo "psutil is not installed. Installing..."
    docker exec -it spark-master pip install psutil
    
    if [ $? -eq 0 ]; then
        echo "psutil is installed"
    else
        echo "psutil installation failed. Abort"
        exit 1
    fi
fi

docker exec -it spark-master spark-submit --master spark://spark-master:7077 $FILEPATH
