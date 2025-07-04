from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
import json

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋 Нажми кнопку 💈 *Записаться* в левом нижнем углу.",
        parse_mode="Markdown"
    )

# Обработка WebApp данных
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.web_app_data:
        try:
            data = json.loads(update.message.web_app_data.data)
            specialist = data.get("specialist", "неизвестно")
            date_str = data.get("date", "неизвестно")
            time_str = data.get("time", "неизвестно")

            # Преобразование даты
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                weekdays = {
                    "Monday": "Понедельник",
                    "Tuesday": "Вторник",
                    "Wednesday": "Среда",
                    "Thursday": "Четверг",
                    "Friday": "Пятница",
                    "Saturday": "Суббота",
                    "Sunday": "Воскресенье",
                }
                formatted_date = weekdays[date_obj.strftime("%A")] + " " + date_obj.strftime("%d.%m.%Y")
            except:
                formatted_date = date_str

            message = (
                f"Мои поздравления 🙌🏽 Вы записались на *{formatted_date}* в *{time_str}* ✅\n"
                f"Мастер: *{specialist}*\n\n"
                f"*Правило заведения:*\n"
                f" - мы ценим время наших клиентов и чтобы не было накладок большая просьба не опаздывать. "
                f"После задержки более 20 минут мастер не сможет вас принять.\n"
                f" - если вы все же поняли, что не успеваете — пожалуйста, отмените запись нажав кнопку «записаться»."
            )

            await update.message.reply_text(message, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text("❌ Произошла ошибка при обработке записи.")
    else:
        await update.message.reply_text("Нажми кнопку 💈 *Записаться* слева внизу.", parse_mode="Markdown")

# Установка WebApp кнопки в меню
async def setup_webapp_menu_button(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="💈 Записаться",
            web_app=WebAppInfo(url="https://barber-indol-iota.vercel.app/")
        )
    )

# Запуск
def main():
    TOKEN = "8112562910:AAHXA_yu1OEB-JG3Lzdxje0g8-LWyprOslI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.post_init = setup_webapp_menu_button

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
