from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку «Записаться» внизу экрана.")

# Обработка данных из WebApp
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Получены RAW данные:", update.message.web_app_data.data)
        data = json.loads(update.message.web_app_data.data)

        if data.get('action') != 'create_booking':
            await update.message.reply_text("Неизвестный тип запроса")
            return

        # Формируем читабельный список услуг
        services_text = ""
        if data.get('services'):
            services_text = "\n".join(
                f"• {service['title']} - {service['price']} ₸"
                for service in data['services']
            )

        # Формируем сообщение
        message = (
            f"🎉 Новая запись!\n\n"
            f"📅 Дата: {data['date']}\n"
            f"⏰ Время: {data['time']}\n"
            f"🧑‍🎨 Мастер: {data['specialist']}\n"
            f"🏢 Филиал: {data['branch']}\n\n"
            f"💈 Услуги:\n{services_text}\n\n"
            f"👤 Клиент:\n"
            f"• Имя: {data['client']['name']}\n"
            f"• Телефон: {data['client']['phone']}\n"
            f"• Комментарий: {data['client']['comment']}\n\n"
            f"📌 Правила:\n"
            "1. Пожалуйста, не опаздывайте\n"
            "2. При опоздании более 20 минут запись аннулируется\n"
            "3. Для отмены используйте кнопку 'Записаться'"
        )

        await update.message.reply_text(message)
        print("Сообщение успешно отправлено клиенту")

    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        print(error_msg)
        await update.message.reply_text("Произошла ошибка при обработке записи")



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
