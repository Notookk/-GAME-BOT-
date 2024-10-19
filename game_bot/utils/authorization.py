from telegram import ChatMember

def is_admin(update) -> bool:
    """Checks if the user is an admin in the chat."""
    user_id = update.effective_user.id
    chat = update.effective_chat
    chat_member = chat.get_member(user_id)
    return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR]
