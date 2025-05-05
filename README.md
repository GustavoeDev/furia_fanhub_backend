# FURIA FanHub Backend

Backend da plataforma FURIA FanHub, desenvolvida para oferecer aos fãs da FURIA uma experiência imersiva durante as partidas ao vivo, com chats em tempo real, mensagens automáticas de apoio e acompanhamento detalhado dos jogos.

🚀 Funcionalidades

```
Gerenciamento de Partidas: Cadastro e controle de partidas com informações como times, placar, mapa, status e horários.

Sistema de Chat: Chats em tempo real vinculados a cada partida, permitindo interação entre os usuários.

Gerenciamento de Competições: Cadastro de campeonatos e associação com os times participantes.

Controle de Times: Cadastro de times com informações como nome e logo.
```

🛠️ Tecnologias Utilizadas

```
Django REST Framework

SQLite

Python-SocketIO

Autenticação JWT
```

📁 Estrutura do Projeto

```
accounts/: Gerenciamento de usuários e autenticação.

chats/: Funcionalidades relacionadas aos chats das partidas.

competitions/: Gerenciamento de campeonatos, partidas e times.

core/: Configurações principais do projeto.
```

⚙️ Instalação

Clone o repositório:

```
git clone https://github.com/GustavoeDev/furia_fanhub_backend.git

cd furia_fanhub_backend
```

Crie e ative um ambiente virtual:

```
python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\Scripts\activate  # Windows
```

Instale as dependências:

```
pip install -r requirements.txt
```

Aplique as migrações:

```
python manage.py migrate
```

Inicie o servidor de desenvolvimento:

```
python manage.py runserver
```

📌 Endpoints Principais

```
GET /api/competitions/{competition_id}/matches/{match_id}/: Detalhes de uma partida específica de um campeonato.

GET /api/chats/{match_id}/: Chat associado a uma partida.

POST /api/chats/messages/{chat_id}/: Envia uma mensagem no chat. 

GET /api/competitions/: Lista todos os campeonatos. 

GET /api/competitions/{competition_id}/: Lista os dados de um campeonato específico.

GET /api/teams/{team_id}/: Lista todas as informações de um time específico 
```
