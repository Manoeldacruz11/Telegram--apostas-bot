from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Seu token de bot (NÃO compartilhe publicamente)
TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"

# Comando de boas-vindas
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot ativo! Aguardando oportunidades de apostas seguras...")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()

