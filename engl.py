import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from http.server import BaseHTTPRequestHandler

# Материалы по уровням
MATERIALS = {
    'beginner': """🐣 Начинающий (A1-A2)

Для данного уровня я рекомендую такие материалы:

📝 Лексика:
• English Vocabulary In Use: https://vk.com/doc138611568_629793650
• Outcomes Beginner: https://disk.yandex.ru/d/k8ydGTz5WBQN7g
• Outcomes Elementary: https://disk.yandex.ru/d/Z_-pkpbxgWibvA
• Outcomes Pre-Intermediate: https://disk.yandex.ru/d/gBBwQSCEm9P_lw

📚 Грамматика:
• English Grammar In Use: https://vk.com/doc241436692_682916970
• My Grammar Lab A1-A2: https://drive.google.com/file/d/1KM09Ho5zgsLBj_wL0O97-ANO3TkDw-F1/view
• English File: https://disk.yandex.ru/d/5qtzvweu3Hus7g

🎤 Говорение:
• Speak Out: https://disk.yandex.ru/d/fid3nycJcdrCcA

🧏‍♀️ Аудирование (доп):
• Фильмы и сериалы в оригинале: https://inoriginal.net/""",
    
    'intermediate': """🌱 Средний (B1-B2)

Для данного уровня я рекомендую такие материалы:

📝 Лексика:
• English Vocabulary In Use: https://vk.com/doc138611568_629793645
• Outcomes Intermediate: https://disk.yandex.ru/d/EQ-uPgfoUNl89Q
• Outcomes Upper-Intermediate: https://disk.yandex.ru/d/46TxuCCjDzDqFw

📚 Грамматика:
• English Grammar In Use: https://vk.ru/doc241436692_682916965
• Destination B1: https://vk.ru/doc229619217_590305691
• Destination B2: https://vk.ru/doc229619217_590305740
• My Grammar Lab B1-B2: https://drive.google.com/file/d/18zlut8jtQVm0cZ_VxFwY4_bXj_00NQ-Q/view
• English File: https://disk.yandex.ru/d/5qtzvweu3Hus7g

🎤 Говорение:
• Speak Out: https://disk.yandex.ru/d/fid3nycJcdrCcA

🧏‍♀️ Аудирование (доп):
• Фильмы и сериалы в оригинале: https://inoriginal.net/""",
    
    'advanced': """🌳 Продвинутый (C1-C2)

Для данного уровня я рекомендую такие материалы:

📝 Лексика:
• Outcomes Advanced: https://disk.yandex.ru/d/t2cf9dv8CtLaiQ
• English Vocabulary In Use: https://vk.com/doc138611568_629793655

📚 Грамматика:
• English Grammar In Use: https://vk.com/doc241436692_682916979
• Destination C1-C2: https://vk.ru/doc229619217_590305824
• English File: https://disk.yandex.ru/d/5qtzvweu3Hus7g

🎤 Говорение:
• Speak Out: https://disk.yandex.ru/d/fid3nycJcdrCcA

🧏‍♀️ Аудирование (доп):
• Фильмы и сериалы в оригинале: https://inoriginal.net/"""
}

AI_TOOLS = """🤖 Нейросети для изучения английского языка

🗣️ Разговорная практика и произношение:
• ChatGPT - практика письменного и устного диалога
• Elsa Speak - коррекция акцента и произношения
• Soul Machines - практика с AI-аватарами
• GetPronounce - тренировка фонетических навыков
• Speechling - анализ произношения, интонации, ритма

📚 Изучение слов и лексики:
• Duolingo & Max - адаптивные платформы
• Quizlet - запоминание слов с флеш-карт
• YouGlish - контекстные примеры из видео
• PlayPhrase.me - примеры из фильмов и сериалов

📝 Грамматика и письмо:
• ChatGPT - проверка грамматики и редактирование
• Quillbot AI - проверка, перефразировка, перевод
• Grammar Check - проверка грамматики

👂 Аудирование и восприятие речи:
• Natural Readers - озвучивание текста
• YouGlish - разные акценты и скорость речи
• PlayPhrase.me - произношение в контексте

⚠️ Важно помнить, что эффективное использование ИИ начинается с качественных промптов (запросов или инструкций для нейросети)! 🌟"""

# PDF файл с промптами закодирован в base64 (добавьте свой файл)
# Инструкция: используйте online base64 encoder для конвертации PROMT.pdf
PROMPTS_PDF_URL = "https://github.com/catthecat3/engbot18/blob/main/PROMT.pdf"  # Или загрузите на GitHub и укажите ссылку

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение при старте бота"""
    user = update.effective_user
    first_name = user.first_name if user.first_name else "друг"
    
    welcome_text = f"""👋 Привет, {first_name}!

Добро пожаловать в English with AI - твоего персонального помощника в изучении английского языка с помощью искусственного интеллекта!

Для начала мне необходимо узнать твой уровень владения английским языком 🌟

Расскажи, пожалуйста, какой у тебя сейчас уровень английского?

Если сомневаешься, советую пройти тест на определение уровня:
https://www.cambridgeenglish.org/test-your-english/"""
    
    keyboard = [
        [InlineKeyboardButton("🐣 Начинающий (A1-A2)", callback_data='level_beginner')],
        [InlineKeyboardButton("🌱 Средний (B1-B2)", callback_data='level_intermediate')],
        [InlineKeyboardButton("🌳 Продвинутый (C1-C2)", callback_data='level_advanced')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def level_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка выбора уровня языка"""
    query = update.callback_query
    await query.answer()
    
    level = query.data.replace('level_', '')
    
    await query.message.reply_text(MATERIALS[level])
    
    keyboard = [
        [InlineKeyboardButton("🤖 Нейросети для изучения", callback_data='show_ai_tools')],
        [InlineKeyboardButton("🔄 Изменить уровень", callback_data='change_level')],
        [InlineKeyboardButton("ℹ️ Главное меню", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Чем сегодня могу помочь? ✨",
        reply_markup=reply_markup
    )

async def show_ai_tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать нейросети для изучения английского"""
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text(AI_TOOLS)
    
    prompts_text = """Важно помнить, что эффективное использование ИИ начинается с качественных промптов (это запрос, команда или набор инструкций, которые пользователь передаёт нейросети для выполнения определённой задачи) 🌟

👩‍🎓 Из-за этого мы добавили файл с лучшими промптами для работы с ИИ (для каждой сферы изучения английского языка)"""
    
    await query.message.reply_text(prompts_text)
    
    # Отправляем ссылку на файл (т.к. на Vercel нельзя хранить файлы)
    await query.message.reply_text(
        f"📄 Скачать промпты: {PROMPTS_PDF_URL}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Возвращайтесь в главное меню:",
        reply_markup=reply_markup
    )

async def change_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Изменить уровень языка"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🐣 Начинающий (A1-A2)", callback_data='level_beginner')],
        [InlineKeyboardButton("🌱 Средний (B1-B2)", callback_data='level_intermediate')],
        [InlineKeyboardButton("🌳 Продвинутый (C1-C2)", callback_data='level_advanced')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Выберите ваш уровень английского:",
        reply_markup=reply_markup
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Главное меню"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📚 Подобрать материалы", callback_data='change_level')],
        [InlineKeyboardButton("🤖 Нейросети для изучения", callback_data='show_ai_tools')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Чем сегодня могу помочь? ✨",
        reply_markup=reply_markup
    )

# Webhook handler для Vercel
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Получаем токен из переменных окружения
        TOKEN = os.environ.get('BOT_TOKEN')
        
        if not TOKEN:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Bot token not configured')
            return
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(level_selected, pattern='^level_'))
        application.add_handler(CallbackQueryHandler(show_ai_tools, pattern='^show_ai_tools$'))
        application.add_handler(CallbackQueryHandler(change_level, pattern='^change_level$'))
        application.add_handler(CallbackQueryHandler(main_menu, pattern='^main_menu$'))
        
        # Обрабатываем обновление
        try:
            update_data = json.loads(post_data.decode('utf-8'))
            update = Update.de_json(update_data, application.bot)
            
            # Запускаем обработку
            import asyncio
            asyncio.run(application.process_update(update))
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

