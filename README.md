# Викторина


В проекте реализованы боты, которые задают вопросы и проверяют ответы пользователя.

[telegram_bot](https://t.me/quiz_dvmnbot) и [vk_bot](https://vk.com/public219929952)

Пример работы telegram бота:
![test](https://github.com/xakars/quiz/assets/73193926/4f79aca3-625b-45ec-a780-568d8b462b0b)


### Как запустить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости

sh
pip install -r requirements.txt

Для развертывания проекта необходимо прописать переменные окружения в файле .env, такие как:
BOT_TOKEN={токен телеграм бота}
VK_TOKEN={токен вконтакте бота}

После выполните следующие команды: 
python3 tg_bot.py
python3 vk_bot.py
