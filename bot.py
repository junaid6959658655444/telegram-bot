from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8664751437:AAEtWJrma9e46KhoNTbbZNKg5GSaYvOgKxI"
ADMIN_ID = 6414433469  # তোমার Telegram ID

# User message handle
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    # Save last user
    context.user_data["last_user"] = user_id

    # Send to admin
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 User ID: {user_id}\n💬 Message: {text}"
    )

# Admin reply handle
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == ADMIN_ID:
        if update.message.reply_to_message:
            text = update.message.text

            # Extract user ID from replied message
            msg = update.message.reply_to_message.text
            user_id = int(msg.split("\n")[0].replace("👤 User ID: ", ""))

            # Send reply to user
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📩 Admin Reply:\n{text}"
            )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))
app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, admin_reply))

app.run_polling()
