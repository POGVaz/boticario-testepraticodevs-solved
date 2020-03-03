# boticario-testepraticodevs-solved
Solução para o desafio back-end do Boticário: https://github.com/grupoboticario/testepraticodevs

Sistema para realização de cadastro e consulta de revendedores e compras feitas, com benefícios dependentes do volume de compras, como cashback.


# Uso
Instalar as dependências deste projeto em um novo ambiente:
```
python -m pip install -r requirements.txt
```
Em seguida, para iniciar o servidor:
```
python manage.py runserver
```
Ou para rodar os testes:
```
python manage.py test
```
__Importante__: Os endpoints requerem autenticação JWT, então para acessá-los manualmente é necessário obter um token e enviar esse token como autorização.
Tokens JWT são concedidos para um par usuário e senha válido e cadastrado no banco de dados como usuário.

Para obter um token (por exemplo, com cURL):
```
curl -X POST -d "username=<seu_username>&password=<sua_senha>" http://localhost:8000/retailer_cashback/get-token-auth/
```

Para enviar o token obtido (por exemplo, para obter a lista de compras):
```
curl -H "Authorization: JWT <seu_token>" http://localhost:8000/retailer_cashback/list-purchases
```
Também é possível acessar
http://localhost:8000/retailer_cashback/get-token-auth/
e utilizar a interface para obter um token com usuário e senha

Para facilitar a depuração e uso da autenticação JWT o seguinte usuário para testes é criado:
- __Username__: 'myUser'
- __Password__: 'myPassword'

## Alternativamente é possível usar Docker-compose (se docker estiver disponível)
Para construir os containers e instalar os requerimentos:
```
docker-compose build
```

Para iniciar os containers:
```
docker-compose up
```
Com isso, Docker vai criar dois containers:
- Wev-server: Onde o back-end vai receber e processar as requisições;
- Database: Onde o postgres vai hospedar e gerenciar o banco de dados.

Para interagir com a aplicação, basta seguir o mesmo procedimento anterior, mas se conectar ao endereço da máquina virtual ao invés de localhost (Endereço default é: _192.168.99.100_)

## Endpoints
- /retailer_cashback/register-retailer -> Para criar novo revendedor(a) com email, senha, nome e cpf
  - POST[email, password, first_name, last_name, cpf]

- /retailer_cashback/validate-retailer -> Para validar usuarios e senha de revendedor(a)
  - GET[username, password]

- /retailer_cashback/register-purchase -> Para registrar nova compra com código, data, valor e cpf
  - POST[code, date, cpf, value]

- /retailer_cashback/list-purchases -> Para pegar uma lista das compras cadastradas.
  - GET[]

- /retailer_cashback/accumulated-cashback -> Para pegar o acumulado de cashback de um usuário com cpf
  - GET[cpf]

# Ferramentas utilizadas

- Python;
  - Django: Framework backend para Python que gerencia o mapeamento de objetos no banco de dados e o processamento de requisições;
  - Django REST: Framework que facilita a construção do backend no esquema REST, utilizando ferramentas de serialização e autenticação;
  - Django REST JWT: Biblioteca para utitilizar o REST com autenticação JWT;
- Postgres: banco de dados de simples conexão com o ORM do Django;
- Docker: Gerenciador de containers, caso for mais conveniente do que um ambiente virtual para rodar a aplicação.

# Requisitos adicionais
Além dos necessário requisitado pelo projeto demonstrado no item "Uso" acima, como registrar um novo revendedor(a) ou consultar a lista de compras, a aplicação se atém a outros requisitos:
- Testes unitários: teste das funções internas e dos modelos (test_service.py e test_model.py);
- Testes de integração: teste de acesso às API (testes em test_views.py funcionam como testes de integração);
- Autenticação JWT por meio de autorização com usuário e senha;
- Logs: o logger do projeto deve encaminhar todos os warnings e errors desejados para a pasta logs.

# Conclusão
A aplicação funciona como backend para registro e consulta simples de revendedores e compras, assim como cálculo de benefícios, mas está longe de estar completa.
Primeiramente seria possível melhorar a forma de cadastro para aceitar mais ou menos campos, conforme for necesário ou conveniente; em seguida seria bem-vindo um sistema de autorização mais completo, com grupos de usuários e permissões personalizadas; por fim, faltaria completar a API com outras operações CRUD, visto que não há forma de atualizar ou deletar entradas sem acesso direto ao banco.
Além disso é sempre benéfico adicionar mais testes, inclusive para as funcionalidades já presentes, principalmente envolvendo excessões e explorando erros e ataques comuns.
