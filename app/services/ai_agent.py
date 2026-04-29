import os
import json
from openai import OpenAI
from app.models.schemas import AIResponse

# Configuração para usar o Ollama (modelo local)
# Você deve ter o Ollama rodando localmente (ex: `ollama run llama3`)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama", # Key dummy necessária pela biblioteca openai
)

def call_ai(parsed_log: str) -> AIResponse:
    """
    Chama a IA local (Ollama) para analisar o log e retorna os dados estruturados.
    """
    
    system_prompt = """
Você é um especialista em análise de logs e depuração de software.
Analise o log fornecido e extraia informações precisas.
Responda APENAS em formato JSON válido contendo exatamente as seguintes chaves e em português:
{
  "tipo_erro": "Tipo do erro (Ex: NullPointerException)",
  "resumo": "Um resumo conciso do problema",
  "causa_raiz": "Possível causa raiz do erro",
  "severidade": "BAIXO, MEDIO ou ALTO",
  "sugestao_solucao": "Sugestão clara de como resolver o problema"
}
Não inclua nenhuma introdução, conclusão ou markdown extra (como ```json), apenas o JSON raw.
"""

    user_prompt = f"Log:\n{parsed_log}"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        # Faz o parse do JSON retornado pela IA para o schema Pydantic
        ai_data = json.loads(content)
        return AIResponse(**ai_data)
        
    except Exception as e:
        # Fallback em caso de erro na chamada ou falha de parse do JSON
        return AIResponse(
            tipo_erro="Erro Desconhecido / Falha na IA",
            resumo=f"Não foi possível processar o log via IA. Detalhe: {str(e)}",
            causa_raiz="Falha na comunicação com o modelo local (Ollama rodando?).",
            severidade="ALTO",
            sugestao_solucao="Verifique se o Ollama está ativo na porta 11434 e o modelo foi baixado (`ollama run llama3`)."
        )
