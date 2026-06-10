import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8617517442:AAHMqoEUfznaAdVYwp35_Gk322ExH4GqIEQ"

CHOICES = {
    "rock": "🪨 Камінь",
    "scissors": "✂️ Ножиці",
    "paper": "📄 Папір",
}

WINS_OVER = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}

scores = {}

def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🪨 Камінь", callback_data="rock"),
            InlineKeyboardButton("✂️ Ножиці", callback_data="scissors"),
            InlineKeyboardButton("📄 Папір", callback_data="paper"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in scores:
        scores[user.id] = {"win": 0, "lose": 0, "draw": 0}

    await update.message.reply_text(
        f"👋 Привіт, {user.first_name}!\n\n"
        f"Обери варіант 👇",
        reply_markup=get_keyboard()
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_choice = query.data
    bot_choice = random.choice(list(CHOICES.keys()))

    if user_choice == bot_choice:
        result = "draw"
        result_text = "🤝 Нічия!"
    elif WINS_OVER[user_choice] == bot_choice:
        result = "win"
        result_text = "🏆 Ти переміг!"
    else:
        result = "lose"
        result_text = "😢 Ти програв!"

    user_id = query.from_user.id
    scores[user_id][result] += 1

    s = scores[user_id]

    await query.message.reply_text(
        f"Ти: {CHOICES[user_choice]}\n"
        f"Бот: {CHOICES[bot_choice]}\n\n"
        f"{result_text}\n\n"
        f"✅ {s['win']}  ❌ {s['lose']}  🤝 {s['draw']}",
        reply_markup=get_keyboard()
    )

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = scores.get(update.effective_user.id, {"win":0,"lose":0,"draw":0})

    await update.message.reply_text(
        f"📊 Рахунок:\n"
        f"✅ {s['win']}\n"
        f"❌ {s['lose']}\n"
        f"🤝 {s['draw']}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CallbackQueryHandler(play))

    print("✅ Бот запущено!")

    app.run_polling()

if __name__ == "__main__":
    main()
