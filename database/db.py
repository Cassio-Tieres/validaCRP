import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from functions.genai_config import gemini_responde
load_dotenv()

CLIENTE = pymongo.MongoClient(os.getenv("MONGO_CON"))
DATA_BASE = CLIENTE["validaCRP"]

def retorna_mensagens_padrao(mensagem):
    global DATA_BASE
    mensagem = mensagem.lower()

    for doc in DATA_BASE["mensagens_padrao"].find():
        if mensagem in doc["pergunta_principal"].lower():
            return doc["resposta"]
    resposta = gemini_responde(mensagem)
    DATA_BASE["mensagens_padrao"].create_index([('expireAt', pymongo.ASCENDING)], expireAfterSeconds=0)
    expiracao = datetime.utcnow() + timedelta(minutes=1)
    DATA_BASE["mensagens_padrao"].insert_one({"pergunta_principal": mensagem.lower(), "resposta": resposta, "expireAt": expiracao})
    return resposta
