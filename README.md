# Ellesse Fashion Bot 👕👖

Telegram-бот для поиска модной одежды на официальном сайте [Ellesse](https://www.ellesse.com). Позволяет быстро находить актуальные коллекции с фильтрацией по размерам и полу.

[![Telegram Bot](https://img.shields.io/badge/Telegram-%40ellesse__sguschonka__bot-blue)](https://t.me/ellesse_sguschonka_bot)

## 🌟 Особенности
- 🔍 Парсинг актуальных товаров с сайта Ellesse в реальном времени
- 👔 Фильтрация по мужской/женской одежде
- 📏 Поддержка всех размеров (от XS до 3XL)
- 💰 Отображение цен с прямыми ссылками на товары
- ⚡ Асинхронная работа для максимальной скорости

## 🛠 Установка и запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка бота
Создайте файл `.env` и добавьте токен:
```ini
BOT_TOKEN=ваш_токен_бота_от_BotFather
```

### 3. Запуск
```bash
python ellesse_bot.py
```

## 📸 Скриншоты интерфейса

| Главное меню | Выбор категории | Результаты поиска |
|-------------|--------------|------------------|
| ![Главное меню](https://github.com/user-attachments/assets/d81e5b71-d425-4a16-9c71-decb686c2837) | ![Выбор размера](https://github.com/user-attachments/assets/ba9852cf-a842-4cee-bcce-11727c13782c) | ![Результаты](https://github.com/user-attachments/assets/35fdf2fd-39fe-4947-8f3e-118988558ef3) |

| ABOUT |
|-----------------------|
| ![Карточка](https://github.com/user-attachments/assets/3212d3f7-59e5-4bda-be89-1bfb02d3c834) |

## 🧰 Технологический стек
- **Python 3.10+**
- **Aiogram 3.x** - фреймворк для Telegram ботов
- **Aiohttp** - асинхронные HTTP-запросы
- **BeautifulSoup4** - парсинг HTML
- **Fake-useragent** - обход защиты сайта

## 📁 Структура проекта
```
.
├── ellesse_bot.py     # Основная логика бота
├── parser.py          # Парсер сайта Ellesse
├── config.py          # Конфигурация (токен)
├── requirements.txt   # Зависимости
├── .env.example       # Пример конфигурации
└── .gitignore
```

## 📜 Лицензия
MIT License © [sguschonka](https://github.com/sguschonka)

---

**👉 Попробуйте бота: [@ellesse_sguschonka_bot](https://t.me/ellesse_sguschonka_bot)**
- На данный момент бот не захостчен(я бедный студент)
