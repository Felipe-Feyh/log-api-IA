import re

def parse_log(raw_log: str) -> str:
    """
    Processa e limpa a string de log bruta antes de enviar para a IA.
    Operações:
    - Remover espaços em branco excessivos
    - Limitar o tamanho máximo do log para evitar exceder os tokens da IA
    """
    if not raw_log:
        return ""
        
    # Remove espaços duplos e quebras de linha múltiplas
    cleaned = re.sub(r'\n+', '\n', raw_log)
    cleaned = re.sub(r' +', ' ', cleaned)
    cleaned = cleaned.strip()
    
    # Truncar o log se for muito longo (ex: max 4000 caracteres)
    MAX_LENGTH = 4000
    if len(cleaned) > MAX_LENGTH:
        cleaned = cleaned[:MAX_LENGTH] + "\n... [TRUNCATED]"
        
    return cleaned
