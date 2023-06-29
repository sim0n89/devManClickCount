# Проверка количества кликов по короткой ссылке bitly и создание коротких ссылок

При вводе ссылки выдается ее короткий вариант для использования. Если ввести короткую ссылку - на экран выведется количество переходов по этой ссылке за все время.

# Установка

В корне проект создать файл .env. В нем необходимо дать значение переменной TOKEN. Ссылка для генерации токена указана на [странице документации Bitly.](https://dev.bitly.com/get_started.html)
Убедитесь что у вас установлен менеджер пакетов pip. Для установки введите в зависимостей введите в терминале `pip install requirements.txt`.

# Запуск

Для запуска в терминале зайдите в папку с проектом и введите `python main.py`.