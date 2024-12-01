from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator

# Configuration du bot
api_id = "24817837"
api_hash = "acd9f0cc6beb08ce59383cf250052686"
bot_token = "7230914838:AAGttYYBpzpSdmiObLY1vL4q56kBHCDQd7Y"
app = Client("translator_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
translator = Translator()

# Langues disponibles pour la traduction
languages = {
    "🇺🇸 English": "en",
    "🇫🇷 French": "fr",
    "🇮🇳 Hindi": "hi",
    "🇸🇦 Arabic": "ar",
    "🇯🇵 Japanese": "ja",
    "🇨🇳 Chinese": "zh-cn",
    "🇩🇪 German": "de"
}

# Dictionnaire pour stocker la langue sélectionnée par chaque utilisateur
user_lang_choice = {}

# Message de démarrage avec formatage corrigé
start_message = """───────────────
├ ‣ [{first_name}](tg://user?id={user_id})
├───────────────────
├ by : @kingcey
╰───────────────────

╭─► 𝙸 𝚊𝚖 𝚊 𝚖𝚎𝚜𝚜𝚊𝚐𝚎 𝚝𝚛𝚊𝚗𝚜𝚕𝚊𝚝𝚒𝚘𝚗 𝚋𝚘𝚝. 📜 𝚂𝚎𝚗𝚍 𝚖𝚎 𝚊 𝚝𝚎𝚡𝚝 ✉️ 𝚊𝚗𝚍 𝚒 𝚠𝚒𝚕𝚕 𝚝𝚛𝚊𝚗𝚜𝚕𝚊𝚝𝚎 𝚒𝚝.🌍 в𝚎𝚏𝚘𝚛𝚎 𝚢𝚘𝚞 𝚜𝚝𝚊𝚛𝚝, 𝚙𝚕𝚎𝚊𝚜𝚎 𝚌𝚕𝚒𝚌𝚔 𝚘𝚗 𝚝𝚑𝚎 𝚋𝚝𝚝𝚘𝚗𝚜 𝚋𝚎𝚕𝚘𝚠 🔘
╰───────────────────
"""

# Boutons de démarrage
start_buttons = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🔍 Choose a language", callback_data="select_language")],
        [
            InlineKeyboardButton("📢 Update", url="https://t.me/hackers_botZ"),
            InlineKeyboardButton("🎴Contact Support", url="https://t.me/kingcey")
        ]
    ]
)

# Commande /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        "https://envs.sh/K6u.jpg",  # URL de l'image
        caption=start_message.format(
            first_name=message.from_user.first_name,  # Nom de l'utilisateur
            user_id=message.from_user.id  # ID de l'utilisateur
        ),
        reply_markup=start_buttons  # Boutons Inline
    )

# Commande /trans
@app.on_message(filters.command("trans"))
async def show_language_options(client, message):
    buttons = [
        [InlineKeyboardButton(text=lang, callback_data=code)]
        for lang, code in languages.items()
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Please choose a language for translation:", reply_markup=reply_markup)

# Commande /help
@app.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = """
To use this bot:
1. Click 🔍 Choose a language to select the language for translation.
2. Send me any text to translate it into your chosen language.
3. For updates, click 📢 Update.
4. If you need support, click Contact Support.

create by : @kingcey
    """
    await message.reply_text(help_text)

# Gestion des sélections via callback
@app.on_callback_query()
async def language_selected(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "select_language":
        buttons = [
            [InlineKeyboardButton(text=lang, callback_data=code)]
            for lang, code in languages.items()
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await callback_query.message.edit_text("Please choose a language for translation:", reply_markup=reply_markup)

    else:
        user_lang_choice[user_id] = data
        await callback_query.message.edit_text("Language selected! Now send me the text you want to translate.")

# Gestion des messages texte (traduction)
@app.on_message(filters.text & ~filters.command("trans"))
async def translate_text(client, message):
    user_id = message.from_user.id
    text = message.text

    if user_id not in user_lang_choice:
        await message.reply_text("Please use /trans to choose a language first.")
        return

    target_language = user_lang_choice[user_id]
    translation = translator.translate(text, dest=target_language)
    language_name = list(languages.keys())[list(languages.values()).index(target_language)]
    await message.reply_text(f"Translation ({language_name}):\n{translation.text}")

    # Réinitialiser la langue choisie après la traduction
    del user_lang_choice[user_id]

# Lancer le bot
app.run()