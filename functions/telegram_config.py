import os
from queue import Queue
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
load_dotenv()

def verifica_texto(mensagem):
    return mensagem.text is not None and not mensagem.text.startswith('/')

async def processa_mensagem(update, context):
    mensagem = update.message.text
    chat_id = update.effective_chat.id
    user = update.message.from_user

    print(f"Mensagem recebida de {user.first_name} no chatID: {chat_id}: {mensagem}")

    if "olá" in mensagem.lower():
        responder = responder_mensagem("Olá! Como posso ajudar você?")
        await context.bot.send_message(chat_id=chat_id, text=responder)

def responder_mensagem(mensagem):
    mensagem = f"Bot diz: {mensagem}"
    return mensagem

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API")).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), processa_mensagem))
    app.run_polling()