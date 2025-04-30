import pymongo

CLIENTE = pymongo.MongoClient("mongodb://localhost:27017/")
DATA_BASE = CLIENTE["validaCRP"]

def retorna_mensagens_padrao(mensagem):
    global DATA_BASE
    for doc in DATA_BASE["mensagens_padrao"].find():
        if mensagem.lower() in doc['variantes'] or mensagem.lower() in doc['pergunta_principal']:
            return doc['resposta']