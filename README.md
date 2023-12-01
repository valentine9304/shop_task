# Проект Grocery Store
Проект продуктового магазина с продуктовой корзиной. У каждого продукта есть своя подкатегория и категория. Продукт можно добавить в корзину. Все продукты в корзине суммируются.

### Как запустить проект
+ Установите и активируйте виртуальное окружение
```
python -m venv venv 
source venv/Scripts/activate
```
+ Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
+ Перейдите в папку grocerystore
+ Выполните миграцию
```
python manage.py migrate
```
+ Запустите проект
```
python manage.py runserver
```

### Примеры API запросов:
+ [GET] /categories/ - Список всех категорий и их подкатегорий
+ [GET] /products/ - Список всех продуктов
+ [POST] /auth/users/ - Регистрация нового пользователя
```json
    "username": "username",
    "password": "password"
```
+ [POST] /auth/jwt/create/ - Выдача jwt token Пользавтелю. 
```json
    "username": "username",
    "password": "password"
```
+ [POST] /products/{ID}/shopping_cart/?quantity=4 - Добавить новый товар ID в коризне в количестве 4, либо изменить количество уже имеющиегося товара в корзине
+ [DELETE] /products/{ID}/shopping_cart/ - удалить товар из корзины
+ [GET] /cart/ - Список всех товаров в корзине
+ [DELETE] /cart/{ID}/ - Удалить определённый товар из корзины
+ [DELETE] /cart/ - Очистить всю корзину

## Автор 
:trollface: Валентин  
