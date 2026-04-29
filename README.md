# Log AI Debugger 🤖🔍

Um agente inteligente construído com **FastAPI** e **Ollama** (Modelos Locais de IA) focado na análise autônoma de logs de aplicação. O sistema identifica erros, diagnostica possíveis causas raízes e sugere soluções estruturadas com base no contexto, além de utilizar uma memória SQLite para identificar casos similares no histórico.

## 🚀 Funcionalidades

- **Análise Semântica de Logs:** Compreende logs de erro (Java, Python, HTTP, etc) utilizando Inteligência Artificial.
- **Upload de Arquivos:** Aceita payloads JSON ou upload de arquivos físicos `.log`/`.txt`.
- **Diagnóstico Estruturado:** Retorna o resumo do problema, a causa raiz, a severidade e a sugestão de solução no formato JSON.
- **Memória de Casos:** Armazena automaticamente o histórico de resoluções.
- **Busca de Similaridade:** Identifica e retorna casos parecidos que já ocorreram no passado para auxiliar no troubleshooting.
- **Privacidade e Custo Zero:** Integrado ao Ollama, garantindo que nenhum log confidencial saia da sua infraestrutura.

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** (Framework Web / API)
- **Ollama** (LLM Host - Padrão: LLaMA 3)
- **SQLite** (Armazenamento em disco leve e rápido)
- **Pydantic** (Validação de Schemas e Payload)
- **OpenAI Python SDK** (Utilizado em formato *drop-in replacement* apontando para o servidor local do Ollama)

---

## ⚙️ Pré-requisitos

Para rodar este projeto na sua máquina, você vai precisar de:

1. **Python** (versão 3.11 ou superior).
2. **Ollama**: [Faça o download e instale o Ollama](https://ollama.com/download) em sua máquina.

---

## 🏃 Como Executar

### 1. Inicialize o Ollama
Após instalar o Ollama, abra um terminal e baixe o modelo LLaMA 3 (ou outro modelo de sua preferência). O Ollama manterá o serviço de API ativado na porta padrão `11434`.

```bash
ollama run llama3
```
*(Você pode fechar a janela interativa se quiser, o serviço continuará rodando em background).*

### 2. Configure o Ambiente Python
Na raiz do repositório clonado, crie um ambiente virtual e ative-o:

**No Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**No Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
Com o ambiente ativado, instale as bibliotecas necessárias listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Rode a Aplicação
Inicie o servidor de desenvolvimento com o Uvicorn:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível no endereço local. 
O FastAPI gera automaticamente a documentação interativa. Acesse no seu navegador:

👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🧪 Como Testar

A pasta raiz deste projeto contém um arquivo chamado `sample_error.log` com uma Stacktrace realista do Java Spring Boot (`NullPointerException`), que você pode usar para teste imediato.

Existem duas rotas principais no Swagger (`/docs`):

1. **POST `/analyze`**: 
   Passe um JSON contendo o log na chave `"log"`.
   ```json
   {
     "log": "O conteúdo do seu erro aqui"
   }
   ```

2. **POST `/analyze/upload`**: 
   Use o botão de upload para selecionar o arquivo `sample_error.log` da raiz do repositório.

### Exemplo de Resposta do Agente

```json
{
  "summary": "Falha de validação de acesso ao verificar se usuário é ativo devido a objeto nulo.",
  "cause": "A chamada ao método `UserService.findUserByUsername(String)` retornou nulo, causando o NullPointerException na linha 45 de `UserController.java`.",
  "solution": "Verifique se o usuário 'admin' existe no banco de dados e adicione uma validação no controller (ex: `if (user != null)`) antes de chamar `user.isActive()`.",
  "severity": "ALTO",
  "similar_cases": []
}
```

## 🏗️ Estrutura do Projeto

```text
/
├── app/
│   ├── database/
│   │   └── db.py                 # Setup do SQLite
│   ├── models/
│   │   └── schemas.py            # Modelos Pydantic (In/Out)
│   ├── routes/
│   │   └── analyze.py            # Rotas e Endpoints do FastAPI
│   ├── services/
│   │   ├── ai_agent.py           # Conexão e prompt builder para o Ollama
│   │   ├── diagnosis_service.py  # Orquestrador do fluxo da IA
│   │   ├── log_parser.py         # Tratamento e truncamento da string de log
│   │   └── memory_service.py     # Lógica do Repository/CRUD do SQLite
│   └── main.py                   # Ponto de entrada FastAPI e Lifespan Events
├── requirements.txt              # Dependências
├── sample_error.log              # Arquivo de erro de exemplo
└── README.md                     # Documentação do projeto
```
