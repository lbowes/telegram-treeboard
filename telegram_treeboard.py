from typing import Tuple, cast, List
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


class Treeboard(): # todo: pass in the options tree here
    def __init__(self, application: Application, tree: todo) -> None:
        self._reset_path()
        # TODO: this should be a tree of options and not a list
        self._WORDS = [ "here", "are", "some", "examples", "of", "options" ]

        application.add_handler(CommandHandler("traverse", self.traverse))

        application.add_handler(CallbackQueryHandler(self.handle_invalid_button, pattern=InvalidCallbackData))
        application.add_handler(CallbackQueryHandler(self.end, pattern="end"))
        application.add_handler(CallbackQueryHandler(self.undo, pattern="undo"))
        application.add_handler(CallbackQueryHandler(self.cancel, pattern="cancel"))
        application.add_handler(CallbackQueryHandler(self.list_button))


    async def traverse(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """The command to initiate the tree traversal."""
        message = ' '.join(self._path)
        updated_keyboard = self._build_keyboard()
        await update.message.reply_text(message, reply_markup=updated_keyboard)


    async def list_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
        await query.answer()

        word, self._path = cast(Tuple[str, List[str]], query.data)
        self._path.append(word)

        message = ' '.join(self._path)
        updated_keyboard = self._build_keyboard()
        await query.edit_message_text(text=message, reply_markup=updated_keyboard)

        # we can delete the data stored for the query, because we've replaced the buttons
        context.drop_callback_data(query)


    async def end(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        message = ' '.join(self._path) + "."
        await query.edit_message_text(text=message)

        self._reset_choices()


    async def undo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        if len(self._path) > 1:
            self._path.pop()

        message = ' '.join(self._path)
        updated_keyboard = self._build_keyboard()
        await query.edit_message_text(text=message, reply_markup=updated_keyboard)

        # we can delete the data stored for the query, because we've replaced the buttons
        context.drop_callback_data(query)


    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Cancels current traversal of tree."""
        query = update.callback_query
        await query.answer()

        self._reset_choices()
        message = ' '.join(self._path)

        chat_id = query.message.chat_id
        message_id = query.message.message_id
        await context.bot.delete_message(chat_id, message_id=message_id)

        # we can delete the data stored for the query, because we've replaced the buttons
        context.drop_callback_data(query)


    async def handle_invalid_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Informs the user that the button is no longer available."""
        await update.callback_query.answer()
        error = "Sorry, I could not process this button click 😕 Please send /traverse to get a new keyboard."
        await update.effective_message.edit_text(error)


    def _build_keyboard(self) -> InlineKeyboardMarkup:
        """Helper function to build the next inline keyboard."""
        # TODO: build the next set of buttons based on the current state of the
        # tree traversal, rather than just using the same set of buttons here
        buttons = [InlineKeyboardButton(w, callback_data=(w, self._path)) for w in self._WORDS]

        done_button = InlineKeyboardButton("✅️", callback_data="end")
        buttons.append(done_button)

        undo_button = InlineKeyboardButton("⏮️", callback_data="undo")
        buttons.append(undo_button)

        cancel_button = InlineKeyboardButton("❌️", callback_data="cancel")
        buttons.append(cancel_button)

        # Convert to 2D list
        keyboard = [buttons[i:i+4] for i in range(0, len(buttons), 4)]

        reply_markup = InlineKeyboardMarkup(keyboard)

        return reply_markup


    def _reset_path(self) -> None:
        """Provide the first item along the tree traversal path (message cannot be empty)."""
        self._path = [ "." ]