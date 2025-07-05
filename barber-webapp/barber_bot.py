from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку «Записаться» внизу экрана.")

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.web_app_data:
            print("✅ Данные получены от WebApp")
            data = json.loads(update.message.web_app_data.data)
            print("📦 JSON:", data)

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
            print("❌ Нет web_app_data")
    except Exception as e:
        print("❌ Ошибка при обработке web_app_data:", e)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 Сообщение:", update.message.text)
    await update.message.reply_text("Я получил сообщение!")

async def setup_webapp_menu_button(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="💈 Записаться",
            web_app=WebAppInfo(url="https://barber-webapp-git-main-adams-projects-62b06f32.vercel.app")
        )
    )

def main():
    TOKEN = "8112562910:AAHXA_yu1OEB-JG3Lzdxje0g8-LWyprOslI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ALL, handle_webapp_data))  # 👈 заменили фильтр
    app.add_handler(MessageHandler(filters.TEXT, echo))  # на всякий случай

    app.post_init = setup_webapp_menu_button

    print("✅ Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
