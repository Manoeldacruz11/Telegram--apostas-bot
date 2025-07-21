import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM")  # Ou coloque direto entre aspas se quiser testar

# /start ou /registrar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if update.effective_chat.type != "private":
        return
    users = context.bot_data.setdefault("users", set())
    users.add(user_id)
    await update.message.reply_text("✅ Registrado para receber apostas seguras!")

# Enviar apostas a cada 15 minutos
async def enviar_apostas(context: ContextTypes.DEFAULT_TYPE):
    apostas = [
        "🔔 Jogo 1 – Mais de 0.5 gol no 1º tempo",
        "🔔 Jogo 2 – Mais de 3.5 escanteios no 1º tempo"
    ]
    for user in context.bot_data.get("users", []):
        for msg in apostas:
            try:
                await context.bot.send_message(chat_id=user, text=msg)
            except Exception as e:
                print(f"Erro ao enviar para {user}: {e}")

# Principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app])
    scheduler.start()

    print("🤖 Bot rodando 24h...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())