import telebot
import math
import json
import os
import sys
import random
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminpanel.settings")

import django
django.setup()

from queries.models import UserQuery  



TOKEN = "8067318459:AAFN9BuOph-rljjtTnpcCu0q3ZVWsqfa7oI"
bot = telebot.TeleBot(TOKEN)

QUOTES_FILE = os.path.join(BASE_DIR, "quotes.json")



def load_quotes() -> list[str]:

    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return ["Цитаты не найдены. Добавьте их в quotes.json."]


def calc(expression: str) -> str:

    expression = expression.replace("^", "**")
    allowed_names = {
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "round": round,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "pow": math.pow,
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
     
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"
    except Exception:
        return "Ошибка: неверное выражение"


def log_query(message, command: str, result: str = "") -> None:

    UserQuery.objects.create(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
        command=command,
        text=message.text or "",
        result=result,
    )



@bot.message_handler(commands=["start"])
def handle_start(message):
    name = message.from_user.first_name or "друг"
    text = (
        f"Привет, {name}! 👋\n\n"
        "Я многофункциональный бот-помощник. Вот что я умею:\n\n"
        "🧮 Просто напиши выражение — и я посчитаю (например: 2+2)\n"
        "💬 /quote — случайная цитата\n"
        "📋 /history — история вычислений\n"
        "🗑 /clear — очистить историю\n"
        "ℹ️ /help — справка\n"
    )
    bot.reply_to(message, text)
    log_query(message, "/start", "sent welcome")


@bot.message_handler(commands=["help"])
def handle_help(message):
    text = (
        "📖 Справка по командам:\n\n"
        "2+2 — калькулятор (поддерживает: +−×÷, sqrt, sin, cos, pi, e, log)\n"
        "/quote — случайная мудрая цитата\n"
        "/history — последние 10 вычислений\n"
        "/clear — очистить историю вычислений\n"
    )
    bot.reply_to(message, text)
    log_query(message, "/help", "sent help")


@bot.message_handler(commands=["calc"])
def handle_calc(message):
    expression = message.text[5:].strip()
    if not expression:
        bot.reply_to(message, "✏️ Укажи выражение. Пример: /calc 2 + 2")
        log_query(message, "/calc", "empty expression")
        return

    result = calc(expression)
    reply = f"🧮 {expression} = *{result}*"
    bot.reply_to(message, reply, parse_mode="Markdown")
    log_query(message, "/calc", result)


@bot.message_handler(commands=["quote"])
def handle_quote(message):
    quotes = load_quotes()
    quote = random.choice(quotes)
    bot.reply_to(message, f"💬 {quote}")
    log_query(message, "/quote", quote[:100])





@bot.message_handler(commands=["history"])
def handle_history(message):

    entries = (
        UserQuery.objects
        .filter(user_id=message.from_user.id, command="/calc")
        .order_by("-created_at")[:10]
    )
    if not entries:
        bot.reply_to(message, "📋 История пуста.")
        return

    lines = [f"[{e.created_at.strftime('%d.%m %H:%M')}] {e.text[6:].strip()} = {e.result}"
             for e in reversed(entries)]
    bot.reply_to(message, "📋 История вычислений:\n\n" + "\n".join(lines))
    log_query(message, "/history", f"returned {len(lines)} entries")


@bot.message_handler(commands=["clear"])
def handle_clear(message):
    deleted, _ = UserQuery.objects.filter(
        user_id=message.from_user.id, command="/calc"
    ).delete()
    bot.reply_to(message, f"🗑 История очищена ({deleted} записей удалено).")
    log_query(message, "/clear", f"deleted {deleted}")



@bot.message_handler(func=lambda m: True)
def handle_unknown(message):
    text = message.text.strip()
    
    import re
    is_math = bool(re.match(r'^[\d\s\+\-\*\/\^\(\)\.a-zA-Z]+$', text))
    
    if is_math:
        result = calc(text)
        reply = f"🧮 {text} = {result}"  # ← убрали звёздочки и parse_mode
        bot.reply_to(message, reply)      # ← без Markdown
        log_query(message, "/calc", result)
    else:
        bot.reply_to(message, "❓ Неизвестная команда. Напиши /help чтобы увидеть список команд.")
        log_query(message, "unknown", text[:100])


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
