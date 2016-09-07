Выполнила Кускова Наталия. <br>
<br>
Django проект "image_search" разработан на python 3.5 <br>
Установить виртуальное окружение из /image_search/requirements.txt<br>
<br>
Scrapy проект "image_parser" разработан на python 2.7 <br>
Установить виртуальное окружение из /image_parser/requirements.txt<br>
<br>
Документация для "image_search": /image_search/docs/_build/html/index.html <br>
Документация для "image_parser": /image_parser/docs/_build/html/index.html <br>
<br>
<br>
Для работы необходимо: <br>
1. Запустить сервер Django из папки /image_search/: <br> 
	python manage.py runserver<br>
2. Запустить спайдеров с помощью honcho из папки /image_parser/: <br>
	honcho start <br>
3. Запустить сервер /image_search/search_img/server.py: <br>
	python server.py <br>

