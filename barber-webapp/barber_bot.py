from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

TOKEN = "8112562910:AAHXA_yu1OEB-JG3Lzdxje0g8-LWyprOslI"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку 'Записаться' внизу экрана.")


async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📥 Обработка данных от WebApp:")
    print("➡️ update.message:", update.message)
    print("➡️ update.message.web_app_data:", update.message.web_app_data)

    try:
        if update.message.web_app_data:
            print("✅ Получены данные из WebApp")
            data = json.loads(update.message.web_app_data.data)
            print("📦 Полученные данные:", data)

            # Формируем список услуг
            services = data.get("services", [])
            services_text = "\n".join(f"— {s['title']} ({s['price']} ₸)" for s in services) if services else "—"

            # Формируем финальное сообщение
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

            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        else:
            print("❌ web_app_data отсутствует")
    except Exception as e:
        print("❌ Ошибка обработки данных:", e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Произошла ошибка при обработке данных 😞")


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

    # 🛠️ Правильный фильтр для обработки WebApp данных
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    app.post_init = setup_menu
    print("✅ Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
