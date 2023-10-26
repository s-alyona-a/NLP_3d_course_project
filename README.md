# Поиск по корпусу
Сайт: https://for0study0projects.pythonanywhere.com

**1. Preprocessing**
   
   Сначала были собраны тексты авторов российских детективов с сайта Lib.ru (http://lib.ru/RUSS_DETEKTIW/) (фунцции get_href, get_text).
   После чего с помощью nltk были взяты предложения и слова, которые потом обрабатывались библиотекой pymorphy, и записаны в файлы .csv.

**2. Search function**
**3. Website**

Веб-страница, построенная на базе Django, включает в себя:
- окно поиска
- модальное окно с краткой информацией о проекте и о том, как составлять запросы (кнопка "помощь")
- зону выдачи результатов: для каждого текста, в котором было зафиксировано совпадение с запросом, создается карточка. На эту карточку выводятся все предложения текста, которые удовлетворяют запросу. Слова, соответствующие запросу, выделяются цветом и жирным курсивным начертанием. Также все найденые словоформы/словосочетания выводятся отдельным блоком справа более крупным шрифтом, чтобы пользователь мог посмотреть на n-граммы отдельно (например, в случае, если ему необходимо определить сочетаемость слова в запросе)

*Что было сделано:*
1) На основе csv-файлов были созданы модели. Для этого были написаны функции конвертации csv-файлов в модели;
2) Была встроена и адаптирована под Django функция поиска;
3) Была реализована пагинация: результаты запроса (которых может быть достаточно много, например, если мы просто задаем POS-тег) помещаются в кэш-таблицу, эти результаты делятся по страницам и при перелистывании достаются оттуда (так можно избежать повторной отправки запроса —> экономим время)
4) Была написана функция для нахождения всех вхождений запроса и их выделений (выделяются желтым цветом, жирным курсивом)
В результате выполнения функции поиска мы получаем список с предложениями и словами/словосочетаниями, которые в этих предложениях были отфильтрованы как подпадающие под данный запрос.

Соответственно, в тексте найденные слова могут встречаться со знаками пунктуации, например:
'потому что' - найденная в предложении словоформа
'Я купил кресло потому, что оно удобно'  - предложение с вхождением найденной словоформы
Для того чтобы выделить словоформу, надо сперва найти её в предложении, а потом окружить необходимыми html-тегами, при этом сохранив пунктуацию. Для этого были использованы регулярные выражения.

5) Был создан интерфейс сайта с его концепцией и дизайном
6) Сайт был загружен на сервер PythonAnywhere

*Для ускорения работы сайта были предприняты следующие меры:*
1) Сокращение количества обращений к базе данных (путем создания элемента words_objects = Word.objects.all())
2) Создание кэш-таблицы для хранения результатов выполнения запроса
