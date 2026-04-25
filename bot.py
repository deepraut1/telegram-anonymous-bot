from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
import re

TOKEN = os.getenv("BOT_TOKEN")

# Stylish font
def stylish_text(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    bold = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘵𝘶𝘷𝘸𝘹𝘺𝘻"
    return text.translate(str.maketrans(normal, bold))

# 🚨 Promotion detector
def is_promotion(text):
    if not text:
        return False

    patterns = [
        r"(https?://\S+)",        # any link
        r"(t\.me/\S+)",           # telegram link
        r"(@\w+)",                # username
        r"(\+?\d{10,13})",        # phone number
        r"(wa\.me/\S+)",          # whatsapp
        r"(youtube\.com/\S+)",    # youtube
        r"(instagram\.com/\S+)"   # instagram
    ]

    for p in patterns:
        if re.search(p, text.lower()):
            return True
    return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Loop fix
    if message.from_user.is_bot:
        return

    user = message.from_user

    try:
        # Ignore admin/owner
        member = await context.bot.get_chat_member(message.chat_id, user.id)
        if member.status in ["administrator", "creator"]:
            return

        text = message.text or message.caption or ""

        # 🚨 Check promotion
        if is_promotion(text):
            # Delete message
            await message.delete()

            # Forward to group (admins will see)
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"⚠️ RULE BREAK ALERT\nUser: {user.first_name}\nMessage forwarded below 👇"
            )

            await context.bot.forward_message(
                chat_id=message.chat_id,
                from_chat_id=message.chat_id,
                message_id=message.message_id
            )

            return  # stop further processing

        # ✅ Normal flow

        # Full name
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip().upper()
        styled_name = stylish_text(full_name)

        # Reply support
        reply_id = message.reply_to_message.message_id if message.reply_to_message else None

        # Delete original
        await message.delete()

        # Repost
        if message.text:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"🟣 {styled_name}:\n{message.text}",
                reply_to_message_id=reply_id
            )

        elif message.photo:
            await context.bot.send_photo(
                chat_id=message.chat_id,
                photo=message.photo[-1].file_id,
                caption=f"🟣 {styled_name}:",
                reply_to_message_id=reply_id
            )

        elif message.video:
            await context.bot.send_video(
                chat_id=message.chat_id,
                video=message.video.file_id,
                caption=f"🟣 {styled_name}:",
                reply_to_message_id=reply_id
            )

    except Exception as e:
        print(e)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot is running...")
app.run_polling()
