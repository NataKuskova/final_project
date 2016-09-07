Выполнила Кускова Наталия. <br>
Django проект "image_search" разработан на python 3.5 <br>
Scrapy проект "image_parser" разработан на python 2.7 <br>
Документация для "image_search": /image_search/docs/_build/html/index.html <br>
Документация для "image_parser": /image_parser/docs/_build/html/index.html <br>
Для работы необходимо:
1. Запустить сервер Django: <br> 
python manage.py runserver<br>
2. Запустить 3 спайдера /image_parser/image_parser/spiders: <br>
2.1 scrapy runspider google_spider.py <br>
2.2 scrapy runspider yandex_spider.py <br>
2.3 scrapy runspider instagram_spider.py <br>
3. Запустить сервер /image_search/search_img/server.py: <br>
python server.py <br>

