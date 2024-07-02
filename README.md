# aiogram-quiz-bot

[Quiz bot](https://t.me/send_riko_msg_pls_bot) для Telegram. aiogram3, sqlite3.

## Установка

1) Скопируйте проект:
```bash
git clone https://github.com/Rikoze777/aiogram-quiz-bot
```

2) Создайте `.env` файл в корне проекта и добавьте туда переменные окружения по [примеру](env_example):
```bash
touch .env
```

### Запуск
1) Установите зависимости:
```bash
pip install -r requirements.txt
```

2) Создайте базу данных из [вопросов](questions.py). В результате должен появиться файл `quiz.db`:
```bash
python3 init_db.py
```

2) Запустите бота:
```bash
python3 bot.py
```

