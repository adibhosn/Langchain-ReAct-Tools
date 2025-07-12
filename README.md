# 📄 Instagram Profile Ice Breaker

Este projeto utiliza LangChain e Google Generative AI para buscar, resumir e gerar uma breve descrição sobre perfis do Instagram. A aplicação coleta os dados de perfil e cria um parágrafo descritivo, ideal para gerar resumos ou "ice breakers".

---

## 🚀 Funcionalidades

-  Busca automática de dados públicos de perfis do Instagram.
-  Geração de parágrafos descritivos baseados no perfil.
-  Integração com LangChain Agents e Google Generative AI (Gemini).
-  Uso da técninca ReaAct de LLMs
-  Uso de Tools para permitir uma maior escalabilidade (adição de outros scrapers)
-  Uso de Pydantic para validação de dados.

---

## 🔧 Como Rodar

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Configure seu arquivo .env: 
```
GOOGLE_API_KEY= sua_chave_google_genai
APIFY_TOKEN = sua_chave_apify_token
```


4. Execute o modulo Python:
```
python ice_breaker.py
```
