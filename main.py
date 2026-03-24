import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, GROUP_ID
from handlers.commands import (
    start, stats, ranking, rules, help_command, warn, ban
)
from handlers.messages import handle_message
from handlers.user_management import new_member, left_member
from handlers.moderation import check_message, mute_user, unmute_user
from utils.scheduler import setup_scheduler
from database import Database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

db = Database()

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('stats', stats))
    app.add_handler(CommandHandler('ranking', ranking))
    app.add_handler(CommandHandler('rules', rules))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('warn', warn))
    app.add_handler(CommandHandler('ban', ban))
    app.add_handler(CommandHandler('mute', mute_user))
    app.add_handler(CommandHandler('unmute', unmute_user))
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member))
    
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, check_message), group=0)
    
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))
    
    setup_scheduler(app)
    
    logger.info("Bot został uruchomiony!")
    
    app.run_polling(allowed_updates=['message', 'my_chat_member'])

if __name__ == '__main__':
    main()