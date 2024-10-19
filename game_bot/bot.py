import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from utils import GameState, VoteCounter, WordLoader, is_admin, TokenManager

# Initialize instances for utilities
game_state = GameState()
vote_counter = VoteCounter()
word_loader = WordLoader("data/")  # Folder containing word lists
token_manager = TokenManager("my_secret_key")

# Set up logging for better debugging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_TOKEN' with your bot token
BOT_TOKEN = "YOUR_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a startup message."""
    await update.message.reply_text(
        "Welcome to the Game Bot! Use /game to select and start a game."
    )

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiates game selection with two options."""
    user_id = update.effective_user.id
    if game_state.active_game is not None:
        await update.message.reply_text("A game is already in progress. Please wait.")
        return

    # Set the user who initiated the game
    game_state.active_game = user_id

    keyboard = [
        [InlineKeyboardButton("Spy Game", callback_data="spy_game")],
        [InlineKeyboardButton("Werewolf Hunter", callback_data="werewolf_game")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a game to play:", reply_markup=reply_markup)

async def game_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the game selection."""
    query = update.callback_query
    await query.answer()

    if query.data == "spy_game":
        token = token_manager.generate_token(update.effective_chat.id)
        join_link = f"https://t.me/{context.bot.username}?start={token}"
        await query.edit_message_text(
            f"Spy Game selected! Click [here to join]({join_link}) within the bot chat.", parse_mode="Markdown"
        )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles players joining the game."""
    token = context.args[0] if context.args else None
    if not token or not token_manager.verify_token(update.effective_chat.id, token):
        await update.message.reply_text("Invalid or expired game token.")
        return

    player_id = update.effective_user.id
    player_name = update.effective_user.first_name

    if any(player["id"] == player_id for player in game_state.players):
        await update.message.reply_text("You are already in the game!")
        return

    game_state.add_player(player_id, player_name)
    await update.message.reply_text(f"{player_name} joined the game!")

async def forcestart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the game if minimum players are met."""
    if not is_admin(update):
        await update.message.reply_text("Only admins can use /forcestart.")
        return

    if len(game_state.get_active_players()) < 6:
        await update.message.reply_text("At least 6 players are required to start.")
        return

    keyboard = [
        [
            InlineKeyboardButton("Sports", callback_data="category_sports"),
            InlineKeyboardButton("Animals/Plants/Nature", callback_data="category_animals"),
        ],
        [
            InlineKeyboardButton("Food", callback_data="category_food"),
            InlineKeyboardButton("Character/Profession", callback_data="category_character"),
            InlineKeyboardButton("Random", callback_data="category_random"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a category:", reply_markup=reply_markup)

async def category_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles category selection."""
    query = update.callback_query
    await query.answer()

    category_map = {
        "category_sports": "sports",
        "category_animals": "animals_plants_nature",
        "category_food": "food",
        "category_character": "character_profession",
        "category_random": random.choice(
            ["sports", "animals_plants_nature", "food", "character_profession"]
        ),
    }
    selected_category = category_map[query.data]
    game_state.category = selected_category

    # Assign words and set the spy
    players = game_state.get_active_players()
    spy = random.choice(players)
    game_state.set_spy(spy["id"])

    word_pair = word_loader.get_random_word_pair(selected_category)
    for player in players:
        word = word_pair[1] if player["id"] == spy["id"] else word_pair[0]
        await context.bot.send_message(player["id"], f"Your word is: {word}")

    await query.edit_message_text("The game has started! Give your clues in turns.")

async def pass_turn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Passes the turn to the next player."""
    user_id = update.effective_user.id
    active_players = game_state.get_active_players()

    if user_id != active_players[0]["id"]:
        await update.message.reply_text("It's not your turn!")
        return

    active_players.append(active_players.pop(0))  # Move current player to end of the list
    await context.bot.send_message(active_players[0]["id"], "It's your turn!")

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the voting process."""
    players = game_state.get_active_players()
    keyboard = [
        [InlineKeyboardButton(player["name"], callback_data=f"vote_{player['id']}")] for player in players
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Vote for the spy:", reply_markup=reply_markup)

async def vote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the vote."""
    query = update.callback_query
    await query.answer()
    voted_player_id = int(query.data.split("_")[1])
    vote_counter.cast_vote(query.from_user.id, voted_player_id)

    if len(vote_counter.votes) == len(game_state.get_active_players()):
        majority_vote = vote_counter.get_majority_vote()
        if majority_vote:
            if majority_vote == game_state.spy:
                await query.edit_message_text("Spy found! The players win!")
                game_state.reset()
            else:
                game_state.eliminate_player(majority_vote)
                await query.edit_message_text("Wrong guess! The game continues.")
                vote_counter.reset()

def main():
    """Starts the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("game", game))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("forcestart", forcestart))
    application.add_handler(CommandHandler("pass", pass_turn))
    application.add_handler(CommandHandler("vote", vote))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(game_selection_callback, pattern="^(spy_game|werewolf_game)$"))
    application.add_handler(CallbackQueryHandler(category_selection_callback, pattern="^category_"))
    application.add_handler(CallbackQueryHandler(vote_callback, pattern="^vote_"))

    application.run_polling()

if __name__ == "__main__":
    main()
