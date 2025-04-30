import os
import unicodedata
import re
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from functions.processa_audios import transcreve_audio
from database.db import retorna_mensagens_padrao
load_dotenv()

def verifica_texto(mensagem):
    return mensagem.text is not None and not mensagem.text.startswith('/')

async def processa_mensagem(update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message
    chat_id = update.effective_chat.id
    user = update.message.from_user

    if mensagem.text:
        print(f"Mensagem recebida de {user.first_name} ({user.id}): {mensagem.text}")
        msg = retorna_mensagens_padrao(mensagem.text)
        resposta = responder_mensagem(msg)
        print(resposta)
        await context.bot.send_message(chat_id=chat_id, text=resposta)
    elif mensagem.photo:
        print(f"Imagem recebida de {user.first_name} ({user.id})")
        foto = mensagem.photo[-1]
        file = await context.bot.get_file(foto.file_id)

        nome_pasta = unicodedata.normalize('NFKD', user.first_name).encode('ascii', 'ignore').decode('utf-8')
        nome_pasta = re.sub(r'[^a-zA-Z0-9]', '_', nome_pasta)

        caminho = f"uploads/{nome_pasta}"
        os.makedirs(caminho, exist_ok=True)
        caminho_arquivo = os.path.join(caminho, f"{foto.file_id}.jpg")
        await file.download_to_drive(custom_path=caminho_arquivo)

        resposta = responder_mensagem(f"Imagem recebida!")
        await context.bot.send_message(chat_id=chat_id, text=resposta)
    elif mensagem.voice:
        print(f"Áudio recebido de {user.first_name} ({user.id})")
        audio = mensagem.voice
        file = await context.bot.get_file(audio.file_id)

        nome_pasta = unicodedata.normalize('NFKD', user.first_name).encode('ascii', 'ignore').decode('utf-8')
        nome_pasta = re.sub(r'[^a-zA-Z0-9]', '_', nome_pasta)

        caminho = f"uploads/{nome_pasta}"
        os.makedirs(caminho, exist_ok=True)
        caminho_arquivo = os.path.join(caminho, f"{audio.file_id}.ogg")
        await file.download_to_drive(custom_path=caminho_arquivo)
        transcreve = transcreve_audio(caminho_arquivo)
        recebido = responder_mensagem(f"Áudio recebido!")
        await context.bot.send_message(chat_id=chat_id, text=recebido)
        if transcreve:
            resposta = responder_mensagem(f"Transcrição: {transcreve}")
            await context.bot.send_message(chat_id=chat_id, text=resposta)

def responder_mensagem(mensagem):
    return mensagem

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_API")).build()
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), processa_mensagem))
    app.run_polling()