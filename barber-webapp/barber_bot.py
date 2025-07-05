from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

TOKEN = "ТОКЕН_БОТА"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку 'Записаться' внизу экрана.")

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 Получено сообщение:", update.message)
    try:
        if update.message.web_app_data:
            print("✅ Получены данные из WebApp")
            data = json.loads(update.message.web_app_data.data)
            print("📦 Данные:", data)

            msg = (
                f"Вы записались на {data['date']} в {data['time']}\n"
                f"Мастер: {data['specialist']}"
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        else:
            print("❌ web_app_data отсутствует")
    except Exception as e:
        print("❌ Ошибка:", e)

async def setup_menu(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="💈 Записаться",
            web_app=WebAppInfo(url="https://barber-webapp-git-main-adams-projects-62b06f32.vercel.app")
        )
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ALL, handle_webapp_data))
    app.post_init = setup_menu
    app.run_polling()

if __name__ == "__main__":
    main()
