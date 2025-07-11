# Ice Breaker - Gerador de Resumos de Perfis de Redes Sociais

Um sistema inteligente que utiliza **LangChain** e **Google Gemini** para extrair dados de perfis do Instagram e gerar resumos informativos e profissionais sobre pessoas.

## 🚀 Funcionalidades

- **Scraping Inteligente**: Coleta dados de perfis do Instagram e X (Twitter) usando APIs da Apify
- **Agent Autônomo**: Utiliza LangChain Agents para decidir automaticamente qual rede social consultar
- **Geração de Resumos**: Cria descrições profissionais e concisas usando Google Gemini 2.0
- **Tratamento de Erros**: Sistema robusto com tratamento completo de exceções
- **Fallback Automático**: Se o Instagram falhar, tenta automaticamente o X (Twitter)

## 📋 Pré-requisitos

- Python 3.8+
- Chave da API do Google Gemini
- Token da API do Apify
- Conta no Instagram/X (para os scrapers da Apify)

## 🛠️ Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd Langchain
```

2. **Crie um ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
GOOGLE_API_KEY=sua_chave_google_aqui
APIFY_TOKEN=sua_chave_apify_aqui
```

## 🔑 Obtendo as Chaves de API

### Google Gemini API
1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave de API
3. Copie a chave para o arquivo `.env`

### Apify Token
1. Crie uma conta em [Apify](https://apify.com/)
2. Vá para [Settings > Integrations](https://console.apify.com/account#/integrations)
3. Copie seu token pessoal para o arquivo `.env`

## 📁 Estrutura do Projeto

```
Langchain/
│
├── ice_breaker.py          # Script principal
├── requirements.txt        # Dependências do projeto
├── .env.example           # Exemplo de configuração
├── README.md              # Este arquivo
│
├── agents/
│   ├── __init__.py
│   └── lookup_agent.py     # Agent inteligente para busca de perfis
│
└── tools/
    ├── __init__.py
    ├── instagram_scraper.py # Scraper do Instagram
    └── X_scraper.py        # Scraper do X (Twitter)
```

## 🎯 Como Usar

### Uso Básico

1. **Execute o script principal**
```bash
python ice_breaker.py
```

2. **Modifique o username no código**
```python
# No arquivo ice_breaker.py, linha 14
username = "neymarjr"  # Substitua pelo username desejado
```

### Uso Programático

```python
from agents.lookup_agent import lookup_agent

# Buscar dados do perfil
username = "usuario_exemplo"
result = lookup_agent(username)

if result["status"] == "success":
    profile_data = result["output"]
    print(f"Dados encontrados: {profile_data}")
else:
    print(f"Erro: {result['error']}")
```

## 🔧 Componentes do Sistema

### 1. **Ice Breaker (Arquivo Principal)**
- Coordena todo o fluxo do sistema
- Chama o lookup agent para buscar dados
- Utiliza o Gemini para gerar resumos profissionais

### 2. **Lookup Agent**
- Agent inteligente que decide qual rede social consultar
- Utiliza ReAct (Reasoning + Acting) para tomada de decisões
- Prioriza Instagram, mas faz fallback para X se necessário

### 3. **Scrapers**
- **Instagram Scraper**: Extrai dados de perfis do Instagram
- **X Scraper**: Extrai dados de perfis do X (Twitter)
- Ambos utilizam APIs da Apify para acesso confiável aos dados

## 📊 Dados Extraídos

### Instagram
- Nome completo
- URL do perfil
- Biografia
- Número de seguidores
- Foto do perfil

### X (Twitter)
- Nome
- Username
- Descrição/Bio
- Número de seguidores
- Número de seguindo
- Foto do perfil

## 🎨 Exemplo de Saída

```
Neymar Jr. é um futebolista brasileiro reconhecido mundialmente, atualmente jogando 
no Al-Hilal. Com uma biografia que destaca sua paixão pelo futebol e vida familiar, 
ele mantém uma presença digital substancial com mais de 200 milhões de seguidores. 
Conhecido por sua habilidade excepcional em campo e personalidade carismática, 
Neymar continua sendo uma das figuras mais influentes do esporte internacional.
```

## ⚙️ Configurações Avançadas

### Modificar o Modelo de IA
```python
# No lookup_agent.py ou ice_breaker.py
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # ou "gemini-pro"
    temperature=0.0,           # Criatividade (0.0 a 1.0)
    api_key=api_key
)
```

### Personalizar Prompts
Os prompts podem ser modificados nos arquivos:
- `agents/lookup_agent.py` - Comportamento do agent
- `ice_breaker.py` - Estilo do resumo gerado

## 🐛 Resolução de Problemas

### Erro: "GOOGLE_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme se a chave está correta
- Certifique-se de que não há espaços extras

### Erro: "APIFY_TOKEN não encontrada"
- Verifique se o token do Apify está no `.env`
- Confirme se sua conta Apify está ativa
- Verifique se há créditos disponíveis na conta

### Perfil não encontrado
- Confirme se o username existe na rede social
- Verifique se o perfil é público
- Tente com um username diferente

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🔗 Links Úteis

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Google Gemini API](https://ai.google.dev/)
- [Apify Documentation](https://docs.apify.com/)
- [Instagram Scraper Apify](https://apify.com/apify/instagram-scraper)
- [Twitter Scraper Apify](https://apify.com/epctex/twitter-profile-scraper)

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação das APIs utilizadas
- Verifique os logs de erro para diagnóstico

---

**⚠️ Aviso Legal**: Este projeto é para fins educacionais. Respeite os termos de serviço das plataformas e as leis de privacidade aplicáveis.