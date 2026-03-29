1. Скачайте данные с Kaggle (ССЫЛКА). Разархивируйте. В 3-ем пункте используйте любой CSV файл из данных
2. Поднимите систему с одной data-node `docker compose up --build -d --pull always --wait`
3. Скопируйте данные в кластер `bash scripts/copy_data.sh yellow_tripdata_2016-01.csv`
4. Запустите неоптимизированный эксперимент `bash scripts/run_experiment.sh code/baseline.py`. На первом запуске скрипт установит необходимые пакеты внутрь контейнера spark-master. Результаты эксперимента будут выведены в логах
5. Запустите оптимизированный эксперимент `bash scripts/run_experiment.sh code/optimized.py`. Результаты будут выведены в логах
6. Для чистоты следующего эксперимента полностью перезапустите систему, но с тремя data-nodes:
   1. `docker compose down -v`
   2. `docker compose --profile scale up -d --wait`
   3. `bash scripts/copy_data.sh yellow_tripdata_2016-01.csv`
   4. Эксперимент 1: `bash scripts/run_experiment.sh code/baseline.py`
   5. Эксперимент 2: `bash scripts/run_experiment.sh code/optimized.py`