import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ----------------- LOGGING -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не задан")

# ----------------- DATA -----------------

MATERIALS = {
    "beginner": """🐣 Начинающий (A1-A2)

📝 Лексика:
• English Vocabulary In Use:
https://vk.com/doc138611568_629793650
• Outcomes Beginner:
https://disk.yandex.ru/d/k8ydGTz5WBQN7g
• Outcomes Elementary:
https://disk.yandex.ru/d/Z_-pkpbxgWibvA
• Outcomes Pre-Intermediate:
https://disk.yandex.ru/d/gBBwQSCEm9P_lw

📚 Грамматика:
• English Grammar In Use:
https://vk.com/doc241436692_682916970
• My Grammar Lab A1-A2:
https://drive.google.com/file/d/1KM09Ho5zgsLBj_wL0O97-ANO3TkDw-F1/view
• English File:
https://disk.yandex.ru/d/5qtzvweu3Hus7g

🎤 Говорение:
• Speak Out:
https://disk.yandex.ru/d/fid3nycJcdrCcA

🧏‍♀️ Аудирование:
• Фильмы и сериалы:
https://inoriginal.net/
""",

    "intermediate": """🌱 Средний (B1-B2)

📝 Лексика:
• English Vocabulary In Use:
https://vk.com/doc138611568_629793645
• Outcomes Intermediate:
https://disk.yandex.ru/d/EQ-uPgfoUNl89Q
• Outcomes Upper-Intermediate:
https://disk.yandex.ru/d/46TxuCCjDzDqFw

📚 Грамматика:
• English Grammar In Use:
https://vk.ru/doc241436692_682916965
• Destination B1:
https://vk.ru/doc229619217_590305691
• Destination B2:
https://vk.ru/doc229619217_590305740
• My Grammar Lab B1-B2:
https://drive.google.com/file/d/18zlut8jtQVm0cZ_VxFwY4_bXj_00NQ-Q/view
• English File:
https://disk.yandex.ru/d/5qtzvweu3Hus7g

🎤 Говорение:
• Speak Out:
https://disk.yandex.ru/d/fid3nycJcdrCcA

🧏‍♀️ Аудирование:
• Фильмы и сериалы:
https://inoriginal.net/
""",

    "advanced": """🌳 Продвинутый (C1-C2)

📝 Лексика:
• Outcomes Advanced:
https://disk.yandex.ru/d/t2cf9dv8CtLaiQ
• English Vocabulary In Use:
https://vk.com/doc138611568_629793655

📚 Грамматика:
• English Grammar In Use:
https://vk.com/doc241436692_682916979
• Destination C1-C2:
https://vk.ru/doc229619217_590305824
• English File:
https://disk.yandex.ru/d/5qtzvweu3Hus7g

🎤 Говорение:
• Speak Out:
https://disk.yandex.ru/d/fid3nycJcdrCcA

🧏‍♀️ Аудирование:
• Фильмы и сериалы:
https://inoriginal.net/
"""
}

AI_TOOLS = """🤖 Нейросети для изучения английского языка

🗣 Разговорная практика:
• ChatGPT
• Elsa Speak
• Speechling

📚 Лексика:
• Duolingo
• Quizlet
• YouGlish
• PlayPhrase.me

📝 Грамматика:
• ChatGPT
• Quillbot
• Grammar Check

👂 Аудирование:
• Natural Readers
• YouGlish
• PlayPhrase.me
"""

PROMPTS_PDF_URL = "https://github.com/catthecat3/engbot18/blob/main/PROMT.pdf"

# ----------------- KEYBOARDS -----------------

def level_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🐣 A1-A2", callback_data="level_beginner")],
        [InlineKeyboardButton("🌱 B1-B2", callback_data="level_intermediate")],
        [InlineKeyboardButton("🌳 C1-C2", callback_data="level_advanced")],
    ])

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Нейросети", callback_data="ai")],
        [InlineKeyboardButton("🔄 Сменить уровень", callback_data="change_level")],
    ])

# ----------------- HANDLERS -----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "друг"

    await update.message.reply_text(
        f"👋 Привет, {name}!\n\nВыбери свой уровень английского:",
        reply_markup=level_keyboard()
    )

async def level_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    level = query.data.replace("level_", "")
    await query.message.reply_text(MATERIALS[level])
    await query.message.reply_text(
        "Чем могу помочь дальше? ✨",
        reply_markup=main_menu_keyboard()
    )

async def show_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(AI_TOOLS)
    await query.message.reply_text(f"📄 Промпты:\n{PROMPTS_PDF_URL}")

async def change_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "Выбери уровень:",
        reply_markup=level_keyboard()
    )

# ----------------- MAIN -----------------

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(level_selected, pattern="^level_"))
    app.add_handler(CallbackQueryHandler(show_ai, pattern="^ai$"))
    app.add_handler(CallbackQueryHandler(change_level, pattern="^change_level$"))

    logger.info("✅ Bot started (polling)")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
