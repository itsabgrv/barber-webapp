from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку «Записаться» внизу экрана.")

# Обработка данных из WebApp
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("📨 handle_webapp_data вызван")
        print("Raw update.message:", update.message)

        if update.message.web_app_data:
            print("✅ web_app_data:", update.message.web_app_data.data)
            data = json.loads(update.message.web_app_data.data)
            print("📦 Parsed JSON:", data)

            message = (
                f"Мои поздравления 🙌🏽 Вы записались на {data['date']} в {data['time']} ✅\n"
                f"Мастер: {data['specialist']}\n\n"
                f"Правило заведения:\n"
                " - мы ценим время наших клиентов и чтобы не было накладок большая просьба не опаздывать.\n"
                " - После задержки более 20 минут мастер не сможет вас принять.\n"
                " - если вы все же поняли, что не успеваете пожалуйста отмените запись нажав кнопку «записаться»"
            )

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            print("❌ Нет web_app_data в сообщении")

    except Exception as e:
        print("❌ Ошибка:", e)




# Установка кнопки WebApp в Telegram меню
async def setup_webapp_menu_button(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="💈 Записаться",
            web_app=WebAppInfo(url="https://barber-webapp-git-main-adams-projects-62b06f32.vercel.app")
        )
    )

# Запуск бота
def main():
    TOKEN = "8112562910:AAHXA_yu1OEB-JG3Lzdxje0g8-LWyprOslI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    app.post_init = setup_webapp_menu_button

    print("✅ Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
