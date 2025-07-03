from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋 Нажми кнопку 💈 *Записаться* в левом нижнем углу.",
        parse_mode="Markdown"
    )

# Обработка финального выбора
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.web_app_data:
        data = update.message.web_app_data.data
        try:
            import json
            result = json.loads(data)
            if "branch" in result:
                await update.message.reply_text(
                    f"✅ Запись принята!\n📍 Адрес: {result['branch']}"
                )
            else:
                await update.message.reply_text("❌ Неполные данные.")
        except Exception as e:
            await update.message.reply_text("Ошибка обработки данных.")
    else:
        await update.message.reply_text("Нажми кнопку 💈 *Записаться* слева внизу.", parse_mode="Markdown")

# Кнопка WebApp в меню Telegram
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
