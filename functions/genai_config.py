import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API"))
historico = []

def gemini_responde(mensagem):
    try:
        with open ("prompt/instrucoes.md", "r", encoding="utf-8") as file:
            instrucoes = file.read()
        historico_str = "\n".join([f"Usuário: {msg['usuario']}\nAgente: {msg['agente']}" for msg in historico])
        prompt_completo = f"{instrucoes.strip()}\n\n{historico_str.strip()}\n\nUsuário: {mensagem}\nAgente:"
        resposta = client.models.generate_content(
            model="gemini-2.5-pro-exp-03-25",
            contents=prompt_completo
        )
        historico.append({"usuario": mensagem, "agente": resposta.text})
        return resposta.text
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, não consegui processar sua solicitação."

def gemini_analise_imagem(texto_imagem):
    try:
        with open ("prompt/interprete_dados_da_imagem.md", "r", encoding="utf-8") as file:
            instrucoes = file.read()
        prompt_completo = f"{instrucoes.strip()}\n\n{texto_imagem}"
        resposta = client.models.generate_content(
            model="gemini-2.5-pro-exp-03-25",
            contents=prompt_completo
        )
        return resposta.text
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, não consegui processar sua solicitação."