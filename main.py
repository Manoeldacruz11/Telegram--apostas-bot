import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functools import partial

# Use diretamente seu token, se quiser
TOKEN = os.getenv("TOKEN") or "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"

# Função /start e /registrar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data.setdefault("users", set()).add(update.effective_chat.id)
    await update.message.reply_text("🤖 Bot ativo! Você receberá apostas no privado a cada 15 minutos.")

# Função que envia apostas para os usuários registrados
async def enviar_apostas(app):
    apostas = [
        "🔔 Santos x Palmeiras – Mais de 0.5 gol no 1T",
        "🔔 Real x Barça – Mais de 3.5 escanteios no 1T"
    ]
    users = app.bot_data.get("users", set())
    for user in users:
        for msg in apostas:
            await app.bot.send_message(chat_id=user, text=msg)

# Função principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(partial(enviar_apostas, app), "interval", minutes=15)
    scheduler.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))
    app.run_polling()

if __name__ == "__main__":
    main()
