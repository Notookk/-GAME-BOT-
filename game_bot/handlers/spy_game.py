from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.word_loader import get_random_pair
from utils.game_logic import assign_spy_and_words, is_admin
from config import MIN_PLAYERS, TOPICS

async def start_spy_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_button = InlineKeyboardButton("Join", url=f"https://t.me/{context.bot.username}?start=join_game")
    reply_markup = InlineKeyboardMarkup([[join_button]])

    await update.message.reply_text("Spy Game started! Join the game:", reply_markup=reply_markup)

async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    players = context.user_data.setdefault("players", {})

    if user.id in players:
        await update.message.reply_text("You've already joined the game!")
    else:
        players[user.id] = {"name": user.full_name}
        await update.message.reply_text(f"{user.full_name} has joined the game!")

async def forcestart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if not is_admin(user.id, await context.bot.get_chat_administrators(chat.id)):
        await update.message.reply_text("Only admins can use /forcestart.")
        return

    players = context.user_data.get("players", {})
    if len(players) < MIN_PLAYERS:
        await update.message.reply_text(f"At least {MIN_PLAYERS} players are required to start.")
        return

    topic_buttons = [[InlineKeyboardButton(topic, callback_data=topic)] for topic in TOPICS]
    reply_markup = InlineKeyboardMarkup(topic_buttons)

    await update.message.reply_text("Select a topic:", reply_markup=reply_markup)

async def handle_topic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    topic = query.data

    if topic == "RANDOM":
        topic = random.choice([t for t in TOPICS if t != "RANDOM"])

    assign_spy_and_words(context.user_data["players"], topic)
    await query.edit_message_text(f"Topic selected: {topic}")

    for player_id, data in context.user_data["players"].items():
        await context.bot.send_message(player_id, f"Your word is: {data['word']}")

    await update.callback_query.message.reply_text("Game started! Use voice chat for clues.")
