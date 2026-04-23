from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Loop fix
    if message.from_user.is_bot:
        return

    user = message.from_user

    try:
        # ✅ Check if user is admin/owner
        member = await context.bot.get_chat_member(message.chat_id, user.id)
        if member.status in ["administrator", "creator"]:
            return  # ignore admins

        name = user.first_name

        # Reply support
        reply_id = None
        if message.reply_to_message:
            reply_id = message.reply_to_message.message_id

        # Delete original message
        await message.delete()

        # Re-send message
        if message.text:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"{name}: {message.text}",
                reply_to_message_id=reply_id
            )

        elif message.photo:
            await context.bot.send_photo(
                chat_id=message.chat_id,
                photo=message.photo[-1].file_id,
                caption=f"{name}",
                reply_to_message_id=reply_id
            )

        elif message.video:
            await context.bot.send_video(
                chat_id=message.chat_id,
                video=message.video.file_id,
                caption=f"{name}",
                reply_to_message_id=reply_id
            )

    except Exception as e:
        print(e)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot is running...")
app.run_polling()
