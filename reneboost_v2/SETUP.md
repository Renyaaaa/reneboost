# 🚀 ReneBoost — Инструкция по запуску

## Структура проекта
```
reneboost/
├── public/
│   └── index.html        ← Web App (деплоится на Vercel)
├── bot/
│   ├── bot.py            ← Telegram бот
│   └── requirements.txt
├── vercel.json           ← Конфиг Vercel
└── SETUP.md              ← Эта инструкция
```

---

## Шаг 1 — Деплой Web App на Vercel

1. Зайди на https://vercel.com и войди через GitHub
2. Нажми **"Add New Project"** → **"Import Git Repository"**
   - Если нет репозитория: залей папку через **Vercel CLI**:
     ```bash
     npm i -g vercel
     cd reneboost
     vercel --prod
     ```
3. После деплоя получишь URL вида: `https://reneboost-xxx.vercel.app`
4. Запомни этот URL — он нужен для бота

> ⚠️ Vercel автоматически даёт HTTPS — это обязательное требование Telegram!

---

## Шаг 2 — Настройка бота

### 2a. Открой файл `bot/bot.py` и замени:
```python
BOT_TOKEN = "СЮДА_ВСТАВЬ_ТОКЕН_БОТА"        # токен от @BotFather
WEBAPP_URL = "https://ВАШ_ДОМЕН.vercel.app"  # твой URL с Vercel
ADMIN_ID   = 123456789                        # твой Telegram ID
```

### 2b. Узнать свой Telegram ID:
- Напиши боту @userinfobot — он пришлёт твой ID

---

## Шаг 3 — Подключение Web App к боту через @BotFather

1. Открой @BotFather в Telegram
2. Напиши `/mybots` → выбери своего бота
3. **Bot Settings** → **Menu Button** → **Configure menu button**
4. Введи URL: `https://ВАШ_ДОМЕН.vercel.app`
5. Введи название кнопки: `🚀 Магазин`

> Теперь в чате с ботом появится кнопка меню, открывающая Web App!

---

## Шаг 4 — Запуск бота

```bash
cd reneboost/bot
pip install -r requirements.txt
python bot.py
```

> Для постоянной работы используй **screen**, **tmux** или хостинг (Railway, VPS):
```bash
# screen
screen -S reneboost
python bot.py
# Ctrl+A, D — свернуть
```

---

## Шаг 5 — Проверка

1. Найди своего бота в Telegram
2. Напиши `/start`
3. Нажми кнопку **"Открыть магазин буста"**
4. Выбери пакет → нажми **"Заказать буст"**
5. Бот должен ответить подтверждением, а тебе (админу) прийдёт уведомление

---

## Схема работы

```
Пользователь
    │
    ▼
/start в боте
    │
    ▼
Кнопка "Открыть магазин" (WebApp)
    │
    ▼
Web App (Vercel) — выбор пакета
    │
    ▼
"Заказать буст" → sendData() → бот получает JSON
    │
    ├──▶ Пользователь: "Заказ принят, менеджер свяжется"
    └──▶ Админ: уведомление с данными заказа
```

---

## Частые вопросы

**Q: Web App не открывается?**
A: Убедись что URL в BotFather точно совпадает с Vercel URL (с https://)

**Q: Бот не получает данные заказа?**
A: Web App должен быть открыт именно через Telegram (не браузер)

**Q: Как обновить Web App?**
A: Обнови файл `public/index.html` — Vercel задеплоит автоматически при push в git

---

*ReneBoost © 2025*
