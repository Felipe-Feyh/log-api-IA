from app.services.log_parser import parse_log
from app.services.ai_agent import call_ai
from app.services.memory_service import save_case, search_similar
from app.models.schemas import AnalyzeResponse

def process_diagnosis(raw_log: str) -> AnalyzeResponse:
    """
    Orquestra o fluxo de diagnóstico:
    1. Parse do log
    2. Análise com IA
    3. Busca de casos similares (antes de salvar para evitar trazer o próprio caso)
    4. Salva o caso atual na memória
    5. Constrói a resposta final
    """
    
    # 1. Parse
    parsed_log = parse_log(raw_log)
    
    # 2. IA
    ai_result = call_ai(parsed_log)
    
    # 3. Busca similares na memória (antes de inserir o atual)
    similar_cases = search_similar(ai_result)
    
    # 4. Salvar na memória
    save_case(ai_result)
    
    # 5. Retornar
    return AnalyzeResponse(
        summary=ai_result.resumo,
        cause=ai_result.causa_raiz,
        solution=ai_result.sugestao_solucao,
        severity=ai_result.severidade,
        similar_cases=similar_cases
    )
