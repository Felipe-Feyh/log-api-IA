from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import LogRequest, AnalyzeResponse
from app.services.diagnosis_service import process_diagnosis

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_log_json(request: LogRequest):
    """
    Recebe um log via JSON para análise.
    """
    if not request.log or not request.log.strip():
        raise HTTPException(status_code=400, detail="O log não pode estar vazio.")
        
    try:
        response = process_diagnosis(request.log)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_log_file(file: UploadFile = File(...)):
    """
    Recebe um arquivo .log (multipart/form-data) para análise.
    """
    if not file.filename.endswith(".log") and not file.filename.endswith(".txt"):
         raise HTTPException(status_code=400, detail="O arquivo deve ser um .log ou .txt")
         
    try:
        # Lê o conteúdo do arquivo
        content = await file.read()
        log_text = content.decode("utf-8")
        
        if not log_text.strip():
             raise HTTPException(status_code=400, detail="O arquivo de log está vazio.")
             
        response = process_diagnosis(log_text)
        return response
    except UnicodeDecodeError:
         raise HTTPException(status_code=400, detail="Falha ao decodificar o arquivo. Certifique-se de enviar um arquivo de texto UTF-8 válido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
