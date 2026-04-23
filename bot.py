from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user

    name = user.first_name

    try:
        # Delete original message
        await message.delete()

        # Re-send message anonymously
        if message.text:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"{name}: {message.text}"
            )

        elif message.photo:
            await context.bot.send_photo(
                chat_id=message.chat_id,
                photo=message.photo[-1].file_id,
                caption=f"{name}"
            )

        elif message.video:
            await context.bot.send_video(
                chat_id=message.chat_id,
                video=message.video.file_id,
                caption=f"{name}"
            )

    except Exception as e:
        print(e)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot is running...")
app.run_polling()
