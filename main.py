import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Token do bot
TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"

# Lista de usuários registrados
usuarios_registrados = set()

# Comando /start e /registrar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        usuarios_registrados.add(chat.id)
        await update.message.reply_text("✅ Bot registrado! Você receberá apostas seguras.")
    else:
        await update.message.reply_text("❌ Este bot só funciona em chats privados.")

# Envio automático de apostas seguras
async def enviar_apostas(bot):
    apostas = [
        "⚽ Santos x Palmeiras – Mais de 0.5 gol no 1º tempo",
        "🚩 Real Madrid x Barcelona – Mais de 3.5 escanteios no 1º tempo"
    ]
    for user_id in usuarios_registrados:
        for aposta in apostas:
            try:
                await bot.send_message(chat_id=user_id, text=aposta)
            except Exception as e:
                logging.error(f"Erro ao enviar mensagem para {user_id}: {e}")

# Função principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    # Iniciar agendador
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app.bot])
    scheduler.start()

    # Rodar bot
    await app.run_polling()

# Executar
if __name__ == "__main__":
    asyncio.run(main())