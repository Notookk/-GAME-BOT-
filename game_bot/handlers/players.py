from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def players_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players = context.user_data.get("players", {})
    if not players:
        await update.message.reply_text("No players have joined yet!")
        return

    buttons = [
        InlineKeyboardButton(player["name"], url=f"tg://user?id={player_id}")
        for player_id, player in players.items()
    ]
    reply_markup = InlineKeyboardMarkup.from_column(buttons)

    await update.message.reply_text("Current Players:", reply_markup=reply_markup)
