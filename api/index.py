import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from engl import start, level_selected, show_ai_tools, change_level, main_menu
# ↑ если логика в отдельном файле
# либо просто вставь функции прямо сюда

TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(level_selected, pattern="^level_"))
application.add_handler(CallbackQueryHandler(CallbackQueryHandler(show_ai_tools, pattern="^show_ai_tools$")))
application.add_handler(CallbackQueryHandler(change_level, pattern="^change_level$"))
application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}

@app.get("/")
async def health():
    return {"status": "bot alive"}
