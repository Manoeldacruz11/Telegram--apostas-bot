import logging
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"
CHAT_ID = "SEU_CHAT_ID_AQUI"  # Substitua pelo seu ID pessoal ou de grupo

# Simulando apostas seguras
def encontrar_apostas_seguras():
    return [
        {
            "jogo": "Flamengo x Santos",
            "mercado": "+0.5 Gol 1º Tempo",
            "chance": "87%",
            "odd": "1.53",
            "hora": "19:30",
            "liga": "Brasileirão Série A",
            "link": "https://www.sportingbet.com/"
        },
        {
            "jogo": "Chelsea x Arsenal",
            "mercado": "+3.5 Escanteios 1º Tempo",
            "chance": "83%",
            "odd": "1.58",
            "hora": "16:00",
            "liga": "Premier League",
            "link": "https://www.sportingbet.com/"
        }
    ]

# Envia as apostas
async def enviar_apostas(bot: Bot):
    apostas = encontrar_apostas_seguras()
    for aposta in apostas:
        msg = (
            f"🔥 *Oportunidade Detectada!*\n\n"
            f"*Jogo:* {aposta['jogo']}\n"
            f"*Mercado:* {aposta['mercado']}\n"
            f"*Probabilidade:* {aposta['chance']}\n"
            f"*Odd:* {aposta['odd']}\n"
            f"*Horário:* {aposta['hora']}\n"
            f"*Liga:* {aposta['liga']}\n\n"
            f"📌 [Aposte agora]({aposta['link']})"
        )
        await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

# Comando /start
async def start(update, context):
    await update.message.reply_text("👋 Bot de apostas iniciado! Enviarei boas oportunidades aqui!")

# Função principal
async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Envia apostas a cada hora
    async def loop_apostas():
        bot = Bot(token=TOKEN)
        while True:
            await enviar_apostas(bot)
            await asyncio.sleep(3600)

    asyncio.create_task(loop_apostas())
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())