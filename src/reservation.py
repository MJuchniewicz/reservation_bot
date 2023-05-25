
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from functools import partial

from typing import Dict

from config.config import TELEGRAM_BOT_TOKEN

from helpers.validation import is_valid_email
from helpers.calendar.calendar_handlers import calendar_handler, inline_handler
from helpers.airtable import ask_save_to_db
from helpers.logger import logger


table_name = "reservations"
ask_save_to_db_with_table = partial(ask_save_to_db, table_name=table_name)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, CHOICE_STATE, CREATE_RESERVATION, EMAIL, PHONE_NUMBER, FINISH_RESERVATION, NAME = range(
    9)

reply_keyboard = [
    ["Create a reservation"],
    ["Quit"],
]
markup = ReplyKeyboardMarkup(
    reply_keyboard, one_time_keyboard=False, resize_keyboard=True)

default_keyboard = [
    ["Cancel"],
    ["Start over"],
]

default_markup = ReplyKeyboardMarkup(
    default_keyboard, one_time_keyboard=False, resize_keyboard=True)


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Resets the conversation and starts the reservation process from beginning."""
    context.user_data.clear()
    await update.message.reply_text(
        "User data has been cleared. What would you like to start with?", reply_markup=markup,
    )
    return CHOOSING


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Hi! Welcome to the reservation system. What would you like to start with?",
        reply_markup=markup,
    )
    return CHOOSING


async def create_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Please provide name of the guest.", reply_markup=default_markup
    )

    return NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text(
        "Provide email address.", reply_markup=default_markup
    )

    return EMAIL


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    markup = ReplyKeyboardMarkup(
        [["Finish reservation", "Start over"]], one_time_keyboard=True, resize_keyboard=True)

    email = update.message.text
    if is_valid_email(email):
        context.user_data["email"] = email
        await update.message.reply_text(
            "Confirm and save reservation or cancel and start over", reply_markup=markup
        )
        return FINISH_RESERVATION
    else:
        await update.message.reply_text(
            "Provide valid email address.",
        )
        return EMAIL


async def ask_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone_number = update.message.text
    context.user_data["phone_number"] = phone_number

    await update.message.reply_text(
        "Provide phone number of the guest.",
    )

    return FINISH_RESERVATION


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    return TYPING_REPLY


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


async def reservation_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    markup = ReplyKeyboardMarkup(
        [['Yes', 'No']], one_time_keyboard=True, resize_keyboard=True)

    if user_data:
        await update.message.reply_text(
            f"Summary of the reservation: {facts_to_str(user_data)}\nDo you want to save the reservation? (Yes/No)",
            reply_markup=markup)
        return CHOICE_STATE
    else:
        await update.message.reply_text(
            "Bye",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user

    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def prompt_again(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt the user again with the same question."""
    await update.message.reply_text(
        "Please choose an option from the keyboard.",
        reply_markup=markup,
    )
    return CHOOSING
