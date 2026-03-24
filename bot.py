from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = "8664751437:AAEtWJrma9e46KhoNTbbZNKg5GSaYvOgKxI"
ADMIN_ID = 6414433469

users = set()
user_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text("আপনি বটে যুক্ত হয়েছেন ✅")

async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    users.add(user.id)

    sent = await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=msg.chat_id,
        message_id=msg.message_id
    )

    user_messages[sent.message_id] = user.id

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id

        if reply_id in user_messages:
            user_id = user_messages[reply_id]
            await context.bot.send_message(chat_id=user_id, text=update.message.text)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text.replace("/broadcast ", "")

    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=text)
        except:
            pass

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user))
app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, handle_admin_reply))
app.add_handler(CommandHandler("broadcast", broadcast))

print("Bot Running...")
app.run_polling()
