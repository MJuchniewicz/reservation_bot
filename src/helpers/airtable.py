from datetime import datetime
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from pyairtable import Table

from config.config import AIRTABLE_TOKEN

AIRTABLE_RESERVATION_BASE_ID = 'appwOY3WFhNVYEzrB'


def save_to_airtable(data, table_name):
    """Save the user data to Airtable."""
    table = Table(AIRTABLE_TOKEN, AIRTABLE_RESERVATION_BASE_ID, table_name)

    table.create(data)


async def ask_save_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE, table_name) -> int:
    text = update.message.text.lower()
    user_data = context.user_data
    user_data['timestamp'] = datetime.utcnow().isoformat()

    if text == "yes":
        save_to_airtable(user_data, table_name)
        await update.message.reply_text("Data saved to Airtable.", reply_markup=ReplyKeyboardRemove())
        user_data.clear()

        return ConversationHandler.END
    else:
        await update.message.reply_text("Okay, not saving reservation.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
