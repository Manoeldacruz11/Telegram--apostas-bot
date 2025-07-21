import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM")

# Função /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return  # só responde em chats privados

    context.bot_data.setdefault("users", set()).add(update.effective_chat.id)
    await update.message.reply_text("✅ Você está registrado para receber apostas seguras!")

# Envia apostas a cada 15 minutos
async def enviar_apostas(context: ContextTypes.DEFAULT_TYPE):
    apostas = [
        "🔔 Santos x Palmeiras – Mais de 0.5 gol no 1º tempo ⚽",
        "🔔 Real Madrid x Barcelona – Mais de 3.5 escanteios no 1º tempo 🏟️"
    ]
    for user_id in context.bot_data.get("users", []):
        for aposta in apostas:
            try:
                await context.bot.send_message(chat_id=user_id, text=aposta)
            except Exception as e:
                print(f"Erro ao enviar para {user_id}: {e}")

# Inicia o bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    # Agenda as apostas
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app])
    scheduler.start()

    print("✅ Bot iniciado com sucesso!")
    app.run_polling()

if __name__ == "__main__":
    main()