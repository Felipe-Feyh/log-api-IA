import hashlib
from typing import List
from app.database.db import get_db_connection
from app.models.schemas import AIResponse, SimilarCase

def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def save_case(ai_result: AIResponse) -> int:
    """
    Salva a análise no banco de dados SQLite.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    error_hash = generate_hash(ai_result.tipo_erro + ai_result.resumo)
    
    cursor.execute(
        """
        INSERT INTO log_cases (error_hash, summary, cause, solution)
        VALUES (?, ?, ?, ?)
        """,
        (error_hash, ai_result.resumo, ai_result.causa_raiz, ai_result.sugestao_solucao)
    )
    
    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return inserted_id

def search_similar(ai_result: AIResponse) -> List[SimilarCase]:
    """
    Busca casos similares usando LIKE simples no resumo ou no hash do erro.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Busca por casos onde o resumo tem alguma similaridade textual (simples) ou mesmo hash
    error_hash = generate_hash(ai_result.tipo_erro + ai_result.resumo)
    
    # Exemplo: pega as duas primeiras palavras importantes do resumo
    words = ai_result.tipo_erro.split()
    like_query = f"%{words[0]}%" if words else "%error%"
    
    cursor.execute(
        """
        SELECT id, summary, cause, solution
        FROM log_cases
        WHERE error_hash = ? OR summary LIKE ?
        LIMIT 3
        """,
        (error_hash, like_query)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    similar_cases = []
    for row in rows:
        similar_cases.append(
            SimilarCase(
                id=row['id'],
                resumo=row['summary'],
                causa=row['cause'],
                solucao=row['solution']
            )
        )
        
    return similar_cases
