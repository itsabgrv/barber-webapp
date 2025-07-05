from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

TOKEN = "8112562910:AAHXA_yu1OEB-JG3Lzdxje0g8-LWyprOslI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку 'Записаться' внизу экрана.")

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 Получено сообщение:", update.message)
    if not update.message.web_app_data:
        print("❌ Это не WebApp данные.")
        return

    try:
        print("✅ Данные WebApp:", update.message.web_app_data.data)
        data = json.loads(update.message.web_app_data.data)
        print("📦 JSON распарсен:", data)

        services = data.get("services", [])
        services_text = "\n".join(f"— {s['title']} ({s['price']} ₸)" for s in services) or "—"

        msg = (
            "🙌 Вы записались!\n\n"
            f"📅 Дата: {data.get('date','—')} в {data.get('time','—')}\n"
            f"👤 Мастер: {data.get('specialist','—')}\n"
            f"📍 Филиал: {data.get('branch','—')}\n\n"
            f"💼 Услуги:\n{services_text}\n\n"
            f"🧑 Имя: {data.get('name','—')}\n"
            f"📞 Телефон: {data.get('phone','—')}\n"
            f"✉️ Email: {data.get('email','—')}\n"
            f"💬 Комментарий: {data.get('comment','—')}"
        )

        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        print("✅ Сообщение успешно отправлено!")

    except Exception as e:
        print("❌ Ошибка при обработке:", e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Произошла ошибка при обработке записи")

async def setup_menu(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="💈 Записаться",
            web_app=WebAppInfo(url="https://barber-webapp-git-main-adams-projects-62b06f32.vercel.app/")
        )
    )
    print("✅ Кнопка меню WebApp установлена.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.post_init = setup_menu
    print("✅ Бот запущен, слушаем WebApp события...")
    app.run_polling()

if __name__ == "__main__":
    main()
