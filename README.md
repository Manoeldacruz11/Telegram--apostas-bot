import logging
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"
CHAT_ID = "@Surperbebebot"

def encontrar_apostas_seguras():
    apostas = [
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
    return apostas

async def enviar_apostas(bot: Bot):
    apostas = encontrar_apostas_seguras()
    for aposta in apostas:
        mensagem = (
            f"🔥 *Oportunidade Detectada!*\n\n"
            f"*Jogo:* {aposta['jogo']}\n"
            f"*Mercado:* {aposta['mercado']}\n"
            f"*Probabilidade:* {aposta['chance']}\n"
            f"*Odd:* {aposta['odd']}\n"
            f"*Horário:* {aposta['hora']}\n"
            f"*Liga:* {aposta['liga']}\n\n"
            f"📌 [Aposte agora na Sportingbet]({aposta['link']})"
        )
        await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="Markdown")

async def start(update, context):
    await update.message.reply_text(
        "👋 Olá! Enviarei apostas seguras sempre que tiver boas oportunidades!"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    bot = Bot(token=TOKEN)
    asyncio.create_task(loop_apostas(bot))
    await app.run_polling()

async def loop_apostas(bot):
    while True:
        await enviar_apostas(bot)
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())