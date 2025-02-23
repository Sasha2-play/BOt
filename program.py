from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  # type: ignore
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes  # type: ignore

# 🔑 Токен бота
BOT_TOKEN = "7427201359:AAHJ1MYYlK4XO9NDZd0GDj8JVMSoGcbJYcA"

# 🔗 Каналы для проверки подписки
CHANNEL_1_ID = -1002316570010  # ID первого канала (замените)
CHANNEL_2_USERNAME = "@odnorazzka"  # Юзернейм второго канала
RESTRICTED_CHANNEL = "https://t.me/sex_v_marshrytke"  # Закрытый канал

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    statuses = {}

    # Проверяем подписку на 1-й канал (по chat_id)
    try:
        member1 = await context.bot.get_chat_member(CHANNEL_1_ID, user_id)
        statuses[CHANNEL_1_ID] = member1.status
    except Exception:
        statuses[CHANNEL_1_ID] = "error"

    # Проверяем подписку на 2-й канал (по username)
    try:
        member2 = await context.bot.get_chat_member(CHANNEL_2_USERNAME, user_id)
        statuses[CHANNEL_2_USERNAME] = member2.status
    except Exception:
        statuses[CHANNEL_2_USERNAME] = "error"

    # 📊 Формируем статус подписки
    message_text = "<b>📢 Статус подписки на каналы:</b>\n\n"
    for channel, status in statuses.items():
        channel_name = "Канал 1" if channel == CHANNEL_1_ID else "Канал 2"
        if status in ["creator", "administrator", "member"]:
            message_text += f"✅ <b>{channel_name}</b>: Подписан\n"
        elif status == "pending":
            message_text += f"⌛ <b>{channel_name}</b>: Заявка отправлена\n"
        else:
            message_text += f"❌ <b>{channel_name}</b>: Не подписан\n"

    # 🔘 Кнопки для подписки и проверки
    keyboard = [
        [InlineKeyboardButton("🔗 Подписаться на канал 1", url="https://t.me/+J_YT_F1TYBYyZTgy")],
        [InlineKeyboardButton("🔗 Подписаться на канал 2", url="https://t.me/odnorazzka")],
        [InlineKeyboardButton("🔄 Проверить подписку", callback_data="check_sub")]
    ]

    # Если пользователь подписан на оба канала – выдаем доступ
    if all(status in ["creator", "administrator", "member"] for status in statuses.values()):
        message_text += "\n🎉 Вы подписаны на оба канала! Вот ваш доступ:"
        keyboard = [[InlineKeyboardButton("🔞 Перейти в закрытый канал", url=RESTRICTED_CHANNEL)]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(message_text, parse_mode='HTML', reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки '🔄 Проверить подписку'."""
    query = update.callback_query
    await query.answer()
    await check_subscription(update, context)  # Повторная проверка подписки

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", check_subscription))
    app.add_handler(CallbackQueryHandler(button_click, pattern="^check_sub$"))

    app.run_polling()

if __name__ == "__main__":
    main()
