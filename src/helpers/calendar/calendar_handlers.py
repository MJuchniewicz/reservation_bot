from telegram import Bot, Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardRemove
from helpers.calendar import telegramcalendar


async def calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please select a date: ",
                                    reply_markup=telegramcalendar.create_calendar())


async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected, date = await telegramcalendar.process_calendar_selection(
        context.bot, update)
    if selected:
        await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                       text="You selected %s" % (
                                           date.strftime("%d/%m/%Y")),
                                       reply_markup=ReplyKeyboardRemove())
