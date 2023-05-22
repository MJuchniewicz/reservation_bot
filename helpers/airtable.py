from datetime import datetime
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from pyairtable import Table

from config.config import AIRTABLE_TOKEN


def save_to_airtable(reservation_data):
    """Save the user data to Airtable."""
    auth_token = AIRTABLE_TOKEN
    base_id = 'appwOY3WFhNVYEzrB'
    table_name = 'reservations'

    table = Table(auth_token, base_id, table_name)

    table.create(reservation_data)


async def ask_save_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.lower()
    user_data = context.user_data
    user_data['timestamp'] = datetime.utcnow().isoformat

    if text == "yes":
        save_to_airtable(user_data)
        await update.message.reply_text("Data saved to Airtable.", reply_markup=ReplyKeyboardRemove())
        user_data.clear()

        return ConversationHandler.END
    else:
        await update.message.reply_text("Okay, not saving reservation.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
