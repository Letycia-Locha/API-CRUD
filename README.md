API de Gerenciamento de Usuários e Lições
Este projeto é uma API RESTful desenvolvida com Django e Django REST Framework para gerenciamento de usuários e lições com conteúdo HTML. A API oferece funcionalidades de CRUD para usuários, autenticação segura e manipulação de conteúdo HTML armazenado no banco de dados.
Funcionalidades Principais
Gerenciamento de Usuários
Criação, leitura, atualização e exclusão de usuários
Autenticação baseada em tokens JWT
Autorização para operações de atualização e exclusão
Manipulação de Lições HTML
Armazenamento de lições com conteúdo HTML
Endpoint para edição do conteúdo HTML das lições
Tecnologias Utilizadas
Django
Django REST Framework
PostgreSQL
JWT para autenticação
Configuração do Ambiente
Clone o repositório:
bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

Crie e ative um ambiente virtual:
bash
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`

Instale as dependências:
bash
pip install -r requirements.txt

Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto e adicione:
text
DEBUG=True
SECRET_KEY=sua_chave_secreta
DATABASE_URL=postgres://usuario:senha@localhost/nome_do_banco

Execute as migrações:
bash
python manage.py migrate

Inicie o servidor:
bash
python manage.py runserver

Endpoints da API
Usuários
POST /usuarios/ - Criar um novo usuário
GET /usuarios/{id}/ - Obter detalhes de um usuário
PUT /usuarios/{id}/ - Atualizar um usuário
DELETE /usuarios/{id}/ - Remover um usuário
Autenticação
POST /api/token/ - Obter token JWT
Lições
POST /licoes/{id}/editar-html/ - Editar o conteúdo HTML de uma lição
Exemplos de Uso
Criar um Usuário
bash
curl -X POST http://localhost:8000/usuarios/ \
     -H "Content-Type: application/json" \
     -d '{"nome": "João Silva", "email": "joao@example.com", "senha": "senha123", "data_de_nascimento": "1990-01-01"}'

Obter Token JWT
bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "joao@example.com", "senha": "senha123"}'

Editar HTML de uma Lição
bash
curl -X POST http://localhost:8000/licoes/1/editar-html/ \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{"conteudo_html": "<div style=\"color: blue;\">Novo conteúdo HTML</div>"}'
