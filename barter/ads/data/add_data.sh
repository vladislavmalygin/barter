#!/bin/bash

# Переход в корневую директорию проекта Django
cd ../../

# Загрузка данных из JSON файла
python manage.py loaddata ads/data/data.json

echo "Данные успешно загружены!"
