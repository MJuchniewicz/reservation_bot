
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from config.config import TELEGRAM_BOT_TOKEN

from helpers.error import error_handler
from helpers.calendar.calendar_handlers import calendar_handler, inline_handler

from reservation import *


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        "^(Create a reservation)$"), create_reservation
                ), MessageHandler(
                    filters.TEXT, prompt_again
                ),
            ],
            NAME:  [
                MessageHandler(filters.TEXT & (
                    ~filters.Regex('^Cancel$')), ask_name),
            ],
            PHONE_NUMBER: [
                MessageHandler(filters.TEXT & (~filters.Regex('^Cancel$')), ask_phone_number)],
            EMAIL: [
                MessageHandler(filters.TEXT & (~filters.Regex('^Cancel$')), ask_email)],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Done$")), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND |
                                     filters.Regex("^Done$")),
                    reservation_summary,
                )
            ],
            CHOICE_STATE: [
                MessageHandler(
                    filters.Regex("^(Yes|No)$"), ask_save_to_db_with_table,
                )
            ],
            FINISH_RESERVATION: [
                MessageHandler(
                    filters.TEXT, done,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done), MessageHandler(
            filters.Regex("^Start over$"), start_over), MessageHandler(
            filters.Regex("^Cancel$"), cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(
        CommandHandler("calendar", calendar_handler))
    application.add_handler(CallbackQueryHandler(inline_handler))
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
