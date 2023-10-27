from telegram.ext import *
import telebot.credentials as credentials
import re

# extract location
def extract_location(text):
    match = re.search(r'\bSomeone fell at (.+)', text, re.IGNORECASE)
    if match:
        location = match.group(1)
        return location
    return None

# send message to the channel
async def send_message(update, context, location):
    chat_id = "-1001835418081" # channel id
    if location: 
        message = "An elderly person has fallen at the location:\n" + location + "\n\nIf you are nearby, please take immediate action to ensure their safety and well-being. Call 995 for medical assistance."

        await context.bot.send_message(chat_id=chat_id, text=message)
    else:
        message = "No location found"
        await context.bot.send_message(chat_id=chat_id, text=message)

# called when a new text message is received by the bot 
# can find the credentials of the bot in the credentials.py
async def handle_message(update, context):
    text = update.message.text
    
    location = extract_location(text)
    if location:
        await send_message(update, context, location)

if __name__ == '__main__':
    application = Application.builder().token(credentials.bot_token).build()

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling(1.0)