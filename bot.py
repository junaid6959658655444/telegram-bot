from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = "8664751437:AAEtWJrma9e46KhoNTbbZNKg5GSaYvOgKxI"
ADMIN_ID = 6414433469

user_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আপনি বটে যুক্ত হয়েছেন ✅")

async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    # Send message to admin with user id
    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 User ID: {user.id}\n💬 Message: {msg.text}"
    )

    user_messages[sent.message_id] = user.id

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id

        if reply_id in user_messages:
            user_id = user_messages[reply_id]

            await context.bot.send_message(
                chat_id=user_id,
                text=update.message.text
            )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user))
app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, handle_admin_reply))

print("Bot Running...")
app.run_polling()
