"""
ReneBoost Telegram Bot
Запуск: python bot.py
Требования: pip install python-telegram-bot==20.7
"""

import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
BOT_TOKEN = "СЮДА_ВСТАВЬ_ТОКЕН_БОТА"       # токен от @BotFather
WEBAPP_URL = "https://ВАШ_ДОМЕН.vercel.app" # URL после деплоя на Vercel
ADMIN_ID   = 123456789                       # твой Telegram ID (узнать у @userinfobot)
# ──────────────────────────────────────────────────────────────────────────────

TIER_NAMES = {
    "warrior": "Воин → Грандмастер",
    "epic":    "Эпик → Легенда",
    "myth":    "Миф → Миф Честь",
    "honor":   "Миф Честь → Миф Слава",
    "glory":   "Миф Слава → 1000 ★",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[
        InlineKeyboardButton(
            text="🚀 Открыть магазин буста",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "⚡ *ReneBoost* — профессиональный буст аккаунта в Mobile Legends Bang Bang.\n\n"
        "🏆 Подними свой ранг быстро и безопасно.\n"
        "⭐ Оплата через Telegram Stars или донат.\n"
        "🔒 Гарантия безопасности.\n\n"
        "Нажми кнопку ниже, чтобы выбрать пакет буста 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает данные из Web App когда пользователь нажал 'Заказать'"""
    user = update.effective_user
    raw = update.effective_message.web_app_data.data

    try:
        data = json.loads(raw)
    except Exception:
        await update.message.reply_text("❌ Ошибка обработки заказа. Попробуй ещё раз.")
        return

    if data.get("action") != "order":
        return

    tier_id = data.get("tier", "")
    tier_name = TIER_NAMES.get(tier_id, tier_id)
    price = data.get("price", "?")
    lang = data.get("lang", "ru")

    # Сообщение пользователю
    user_text = (
        f"✅ *Заказ принят!*\n\n"
        f"📦 Пакет: *{tier_name}*\n"
        f"💰 Стоимость: *{price} ⭐ Stars*\n\n"
        f"Наш менеджер свяжется с тобой в течение *15 минут*.\n"
        f"Не передавай данные аккаунта до подтверждения!"
    )
    await update.message.reply_text(user_text, parse_mode="Markdown")

    # Уведомление администратору
    admin_text = (
        f"🔔 *Новый заказ!*\n\n"
        f"👤 Пользователь: [{user.first_name}](tg://user?id={user.id})\n"
        f"🆔 ID: `{user.id}`\n"
        f"📦 Пакет: *{tier_name}*\n"
        f"💰 Цена: *{price} ⭐*\n"
        f"🌐 Язык: {lang}\n\n"
        f"Напиши пользователю и уточни детали!"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление админу: {e}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *ReneBoost* — буст аккаунта MLBB\n\n"
        "/start — открыть магазин\n"
        "/help — помощь\n\n"
        "По вопросам: @ReneBoostSupport",
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
