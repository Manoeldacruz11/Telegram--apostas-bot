import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🔧 Substitua diretamente se quiser (ou defina no Render: TOKEN=seu_token)
TOKEN = os.getenv("TOKEN", "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM")

# Lista de usuários que registraram o bot
users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ativo! Use /registrar para receber apostas.")

async def registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_chat.id)
    await update.message.reply_text("✅ Registrado! Você receberá as apostas automáticas.")

async def enviar_apostas(context: ContextTypes.DEFAULT_TYPE):
    apostas = [
        "🔔 Santos x Palmeiras – Mais de 0.5 gol no 1T",
        "🔔 Real x Barça – Mais de 3.5 escanteios no 1T"
    ]
    for user_id in users:
        for msg in apostas:
            try:
                await context.bot.send_message(chat_id=user_id, text=msg)
            except Exception as e:
                print(f"Erro ao enviar para {user_id}: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # ⏰ Agendador que envia apostas a cada 15 minutos
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app])
    scheduler.start()

    # 🔘 Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", registrar))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
