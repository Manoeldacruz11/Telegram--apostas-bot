import logging
import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler, ApplicationBuilder
import asyncio

# Seu token fornecido pelo BotFather
TOKEN = "8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIvM"  # Token do seu bot
CHAT_ID = None  # Será preenchido no /start

# Exemplo de função que simula uma análise segura (pode futuramente puxar de uma API real)
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

async def enviar_apostas(bot: Bot, chat_id: int):
    apostas = encontrar_apostas_seguras()
    for aposta in apostas:
        mensagem = (
            f"🔥 *Aposta Segura Identificada!*\n\n"
            f"*Jogo:* {aposta['jogo']}\n"
            f"*Mercado:* {aposta['mercado']}\n"
            f"*Probabilidade:* {aposta['chance']}\n"
            f"*Odd:* {aposta['odd']}\n"
            f"*Horário:* {aposta['hora']}\n"
            f"*Liga:* {aposta['liga']}\n\n"
            f"📌 [Aposte agora na Sportingbet]({aposta['link']})"
        )
        await bot.send_message(chat_id=chat_id, text=mensagem, parse_mode="Markdown")

# /start: Registra o chat privado para envio
async def start(update: Update, context):
    global CHAT_ID
    if update.effective_chat.type != "private":
        return await update.message.reply_text("⚠️ Só funciono no privado!")
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("✅ Você foi registrado. Enviarei apostas seguras aqui!")

# Início do bot
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("registrar", start))

    # Início do bot
    bot = Bot(token=TOKEN)
    print("✅ Bot rodando...")

    # Loop para enviar apostas de tempos em tempos
    while True:
        if CHAT_ID:
            await enviar_apostas(bot, CHAT_ID)
        await asyncio.sleep(3600)  # Espera 1 hora até próxima verificação

    await app.run_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())