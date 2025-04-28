import telebot
from config import BOT_TOKEN, CHAT_ID

# Initialize the bot with the token
bot = telebot.TeleBot(BOT_TOKEN)

# Define a function to send a message to the specified chat 
def send_message(message):
    try:
        # Send the message to the specified chat ID
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"Error sending message: {e}")