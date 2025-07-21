import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# === Configurar logging para debug ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Token direto no código (pode usar .env se quiser mais segurança) ===
TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"

# === Lista de usuários registrados ===
usuarios_registrados = set()

# === Comando de início ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if update.effective_chat.type == "private":
        usuarios_registrados.add(chat_id)
        await update.message.reply_text("✅ Bot ativo! Você receberá apostas seguras.")
    else:
        await update.message.reply_text("❌ Este bot só funciona em conversas privadas.")

# === Função que envia as apostas ===
async def enviar_apostas(context: ContextTypes.DEFAULT_TYPE):
    apostas_seguras = [
        "⚽ Santos x Palmeiras – Mais de 0.5 gol no 1º tempo",
        "🚩 Real Madrid x Barcelona – Mais de 3.5 escanteios no 1º tempo",
        # Aqui você pode adicionar sugestões reais do dia se tiver scraping ou API
    ]
    for user_id in usuarios_registrados:
        for aposta in apostas_seguras:
            try:
                await context.bot.send_message(chat_id=user_id, text=aposta)
            except Exception as e:
                logging.error(f"Erro ao enviar para {user_id}: {e}")

# === Função principal ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    # Scheduler para enviar apostas a cada 15 minutos
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app])
    scheduler.start()

    app.run_polling()

# === Rodar ===
if __name__ == "__main__":
    main()
