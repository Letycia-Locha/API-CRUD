# API de Gerenciamento de Usuários e Lições


# Este projeto é uma API RESTful desenvolvida com Django e Django REST Framework para gerenciamento de usuários e lições com conteúdo HTML. 
# A API oferece funcionalidades de CRUD para usuários, autenticação segura e manipulação de conteúdo HTML armazenado no banco de dados.

# Funcionalidades Principais:
* Gerenciamento de Usuários
* Criação, leitura, atualização e exclusão de usuários
* Autenticação baseada em tokens JWT
* Autorização para operações de atualização e exclusão
* Manipulação de Lições HTML
* Armazenamento de lições com conteúdo HTML
* Endpoint para edição do conteúdo HTML das lições
  
# Tecnologias Utilizadas:
* VSCode
* Python 3.12.3
* Django 5.1.2
* Django REST Framework
* PostgreSQL
* JWT para autenticação -
* Configuração do Ambiente - as instruçẽos para configuração do ambiente estão descritas mais abaixo
  (as versões devem ser compativeis com as utilizadas na construção do projeto e estão descritas no documento requirements.txt)

# Pré requisitos:

- Python 3.x: [Download Python](https://www.python.org/downloads/)
- PostgreSQL: [Download PostgreSQL](https://www.postgresql.org/download/)
- (Opcional) VSCode: [Download VSCode](https://code.visualstudio.com/download)
  
# Clone o repositório:

- 1 - utilize sua conta do github para clonar o repositório
- 2 - crie um repositorio próprio com o nome que desejar
- 3 - substitua "seu-usuario" pelo usuário da sua conta
- 4 - substitua "seu-repositorio" pelo titulo que você deu ao seu repositorio
>>   git clone https://github.com/seu-usuario/seu-repositorio.git  <<

no terminal do seu vscode, navegue até o repositório criado para execução do projeto
.
cd seu-repositorio
.
# Crie e ative um ambiente virtual:

Verifique se o python esta instalado na sua máquina executando esse comando no terminal (pode ser o terminal do seu sistema operacional, do vscode, ou qualquer outro da sua preferencia que tenha acesso aos seus diretórios)

python --version

!! importante !! - a versão deve ser compatível com a listada acima, caso não seja, verifique os procedimentos necessários para adequar a versão

com o diretório do seu repositório aberto no terminal, crie e ative o ambiente virtual com os seguintes comandos:

---> Linux
 * python -m venv venv
 * source venv/bin/activate
   
--> No Windows
  * venv\Scripts\activate
.
# Instale as dependências:

o comando deve ser inserido no terminal, dentro do diretório do projeto.

* pip install -r requirements.txt

# Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto e adicione:
>>
* DEBUG=True
* SECRET_KEY=sua_chave_secreta   ------ a sua chave
* DATABASE_URL=postgres://usuario:senha@localhost/nome_do_banco   ----- seu login

Essa etapa de configuração de variáveis de ambiente serve para definir informações sensíveis e configuráveis fora do código-fonte, facilitando a manutenção e segurança do projeto. Ao criar o arquivo .env, você está fornecendo valores específicos para seu projeto de forma segura e flexível. Vamos entender melhor os itens mencionados:

* DEBUG=True:

Ativa o modo de depuração no Django. Quando o DEBUG está True, o Django fornece mensagens detalhadas de erro e logs, úteis durante o desenvolvimento. Em produção, isso deve estar False para evitar a exposição de informações sensíveis.


* SECRET_KEY=sua_chave_secreta:

O SECRET_KEY é utilizado pelo Django para fornecer segurança nas sessões de usuários e na geração de tokens. Ele é uma chave secreta que deve ser única e não deve ser exposta publicamente. Ela garante a integridade de certas funcionalidades, como a criptografia de cookies.

  
* DATABASE_URL=postgres://usuario:senha@localhost/nome_do_banco:


Define a URL de conexão com o banco de dados PostgreSQL. Ela especifica o usuário, senha, endereço do servidor e o nome do banco que o Django vai usar para armazenar e recuperar dados. No formato fornecido, você deve substituir usuario, senha, e nome_do_banco pelos valores corretos do seu ambiente de banco de dados.


Ao usar um arquivo .env, você mantém essas variáveis fora do código fonte, tornando mais fácil mudar essas configurações entre ambientes (desenvolvimento, produção, etc.) sem alterar o código diretamente. Isso também ajuda a manter informações confidenciais (como a SECRET_KEY e as credenciais do banco de dados) seguras.

# Execute as migrações:

python manage.py migrate

# Inicie o servidor:

python manage.py runserver

# Endpoints da API
* Usuários
- POST /usuarios/ - Criar um novo usuário
- GET /usuarios/{id}/ - Obter detalhes de um usuário
- PUT /usuarios/{id}/ - Atualizar um usuário
- DELETE /usuarios/{id}/ - Remover um usuário
* Autenticação
POST /api/token/ - Obter token JWT
* Lições
POST /licoes/{id}/editar-html/ - Editar o conteúdo HTML de uma lição

# Exemplos de Uso
--------------  Criar um Usuário

curl -X POST http://localhost:8000/usuarios/ 
     -H "Content-Type: application/json" 
     -d {
    "username": "lelocha",
    "email": "letycialochavet@gmail.com",
    "password": "senha123",
    "first_name": "Letycia",
    "last_name": "Locha",
    "data_de_nascimento": "1996-02-19"
      }

--------------- Obter Token JWT

curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d  {
          "email": "joao@example.com", 
          "senha": "senha123"
          }

--------------- Editar HTML de uma Lição

curl -X POST http://localhost:8000/licoes/1/editar-html/ \
     -H "Authorization: Bearer seu_token_jwt" \
     -H "Content-Type: application/json" \
     -d '{"conteudo_html": "<div style=\"color: blue;\">Novo conteúdo HTML</div>"}'
