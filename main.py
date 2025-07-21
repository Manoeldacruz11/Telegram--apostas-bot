from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# TOKEN direto no código
TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"

# Comando /start ou /registrar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return  # Só funciona no privado
    context.bot_data.setdefault("users", set()).add(update.effective_chat.id)
    await update.message.reply_text("✅ Você está registrado para receber apostas seguras!")

# Função que envia as apostas
async def enviar_apostas(context: ContextTypes.DEFAULT_TYPE):
    apostas = [
        "🔔 Santos x Palmeiras – Mais de 0.5 gol no 1º tempo ⚽",
        "🔔 Real Madrid x Barcelona – Mais de 3.5 escanteios no 1º tempo 🏟️"
    ]
    for user_id in context.bot_data.get("users", []):
        try:
            for aposta in apostas:
                await context.bot.send_message(chat_id=user_id, text=aposta)
        except Exception as e:
            print(f"Erro ao enviar mensagem para {user_id}: {e}")

# Função principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_apostas, "interval", minutes=15, args=[app])
    scheduler.start()

    print("✅ Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()