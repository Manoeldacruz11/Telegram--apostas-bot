import logging
import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token do seu bot (não compartilhe com ninguém!)
TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"

# Lista de usuários registrados
usuarios_registrados = set()

# Apostas simuladas da casa Sportingbet
def obter_apostas_sportingbet():
    return [
        {
            "jogo": "Flamengo x Santos",
            "mercado": "Mais de 0.5 Gol no 1º Tempo",
            "chance": "87%",
            "odd": "1.53",
            "hora": "19:30",
            "liga": "Brasileirão Série A",
            "link": "https://www.sportingbet.com/"
        },
        {
            "jogo": "Chelsea x Arsenal",
            "mercado": "Mais de 3.5 Escanteios no 1º Tempo",
            "chance": "83%",
            "odd": "1.58",
            "hora": "16:00",
            "liga": "Premier League",
            "link": "https://www.sportingbet.com/"
        }
    ]

# Comando /start e /registrar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    user_id = update.effective_chat.id
    usuarios_registrados.add(user_id)
    await update.message.reply_text("✅ Você foi registrado para receber apostas seguras da Sportingbet!")

# Função para enviar apostas para os usuários
async def enviar_apostas(bot: Bot):
    apostas = obter_apostas_sportingbet()
    for user_id in usuarios_registrados:
        for aposta in apostas:
            mensagem = (
                f"🔥 *Oportunidade Sportingbet!*\n\n"
                f"*Jogo:* {aposta['jogo']}\n"
                f"*Mercado:* {aposta['mercado']}\n"
                f"*Probabilidade:* {aposta['chance']}\n"
                f"*Odd:* {aposta['odd']}\n"
                f"*Horário:* {aposta['hora']}\n"
                f"*Liga:* {aposta['liga']}\n\n"
                f"👉 [Apostar na Sportingbet]({aposta['link']})"
            )
            try:
                await bot.send_message(chat_id=user_id, text=mensagem, parse_mode="Markdown")
            except Exception as e:
                logging.error(f"Erro ao enviar para {user_id}: {e}")

# Função principal
async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    bot = Bot(token=TOKEN)

    async def loop_envio():
        while True:
            await enviar_apostas(bot)
            await asyncio.sleep(3600)  # 1 hora

    # Inicia o loop de envio em segundo plano
    asyncio.create_task(loop_envio())

    print("🤖 Bot rodando 24h...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())