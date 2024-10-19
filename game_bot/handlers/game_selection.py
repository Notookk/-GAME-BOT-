from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import TOPICS

async def game_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    context.user_data["game_master"] = user.id

    keyboard = [[InlineKeyboardButton(game, callback_data=game)] for game in ["Spy Game", "Werewolf Hunter"]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose a game:", reply_markup=reply_markup)

async def handle_game_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != context.user_data.get("game_master"):
        await query.answer("Only the user who initiated the game can choose.")
        return

    game_choice = query.data
    if game_choice == "Spy Game":
        await start_spy_game(update, context)

    await query.answer()
    await query.edit_message_text(f"{game_choice} selected!")
