from telegram import Update, WebAppInfo, MenuButtonWebApp, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json
import logging

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен Telegram бота
TOKEN = "8112562910:AAHXA_yu1OEB-JG3Lzdxje0g8-LWyprOslI"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("➡️ Команда /start")

    user_id = update.effective_user.id
    full_url = f"https://barber-webapp-git-main-adams-projects-62b06f32.vercel.app/?user_id={user_id}"

    keyboard = [
        [KeyboardButton("💈 Записаться", web_app=WebAppInfo(url=full_url))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Добро пожаловать! Нажмите кнопку ниже 👇", reply_markup=reply_markup)

# Обработка данных из WebApp
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.message.web_app_data.data)
        logger.info("✅ Получены данные из WebApp")
        logger.info("📦 Данные: %s", data)

        services = data.get("services", [])
        services_text = "\n".join(f"— {s['title']} ({s['price']} ₸)" for s in services) if services else "—"

        msg = (
            f"🙌 Вы записались!\n\n"
            f"📅 Дата: {data.get('date', '—')} в {data.get('time', '—')}\n"
            f"👤 Мастер: {data.get('specialist', '—')}\n"
            f"📍 Филиал: {data.get('branch', '—')}\n\n"
            f"💼 Услуги:\n{services_text}\n\n"
            f"🧑 Имя: {data.get('name', '—')}\n"
            f"📞 Телефон: {data.get('phone', '—')}\n"
            f"✉️ Email: {data.get('email', '—')}\n"
            f"💬 Комментарий: {data.get('comment', '—')}"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        logger.error("❌ Ошибка при обработке данных WebApp: %s", e)
        await update.message.reply_text("Произошла ошибка при обработке записи 😞")

# Кнопка меню
async def setup_menu(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="💈 Записаться",
            web_app=WebAppInfo(
                url=f"https://barber-webapp-git-main-adams-projects-62b06f32.vercel.app/?user_id={{user_id}}"
            )
        )
    )

    logger.info("✅ Меню WebApp установлено")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.post_init = setup_menu
    logger.info("✅ Бот запущен. Ждём события...")
    app.run_polling()

if __name__ == "__main__":
    main()