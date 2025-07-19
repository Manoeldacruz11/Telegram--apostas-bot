import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data.setdefault("users", set()).add(update.effective_chat.id)
    await update.message.reply_text("🤖 Bot ativo! Use /registrar para receber apostas.")

async def enviar_apostas(context: ContextTypes.DEFAULT_TYPE):
    apostas = [
        "🔔 Santos x Palmeiras – Mais de 0.5 gol no 1T",
        "🔔 Real x Barça – Mais de 3.5 escanteios no 1T"
    ]
    for user in context.bot_data.get("users", []):
        for msg in apostas:
            await context.bot.send_message(chat_id=user, text=msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app.bot])
    scheduler.start()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))
    app.run_polling()

if __name__ == "__main__":
    main()