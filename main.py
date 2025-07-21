import os
import telebot

# Carrega o token da variável de ambiente
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("8186930957:AAHIXGL-860rIhu_vFOs7R0L0qk4U4BhIv")

# Cria o bot
bot = telebot.TeleBot(TOKEN)

# Comando inicial
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "✅ Bot ativo! Você receberá apostas seguras com foco em:\n\n"
        "⚽ Mais de 0.5 gol no 1º tempo\n"
        "🏳️‍🌈 Mais de 3.5 escanteios no 1º tempo\n\n"
        "Casa: Sportingbet"
    )

# Aqui é onde no futuro entraremos com as sugestões automáticas 24h
# Por enquanto, o bot apenas responde com a mensagem inicial

print("✅ Bot iniciado com sucesso.")
bot.infinity_polling()