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
__Importante__: Os endpoints requerem autenticação JWT, então para acessá-los é necessário obter um token e enviar esse token como autorização.
Tokens JWT são concedidos para um par usuário e senha válido e cadastrado no banco de dados como usuário.

Para obter um token (por exemplo, com cURL):


Para enviar o token obtido (por exemplo, para obter a lista de 

## Alternativamente é possível usar Docker-compose
Para iniciar os containers
```
docker-compose up
```
Com isso, Docker vai criar dois containers:
- Wev-server: Onde o back-end vai receber e processar as requisições;
- Database: Onde o postgres vai hospedar e gerenciar o banco de dados.

Para interagir com a aplicação, basta

# Ferramentas utilizadas

- Python;
  - Django: Framework backend para Python que gerencia o mapeamento de objetos no banco de dados e o processamento de requisições;
  - Django REST: Framework que facilita a construção do backend no esquema REST, utilizando ferramentas de serialização e autenticação;
  - Django REST JWT: Biblioteca para utitilizar o REST com autenticação JWT;
- Postgres;
- Docker: Gerenciador de containers, caso for mais conveniente do que um ambiente virtual para rodar a aplicação.

# Requisitos atendidos
- Registro de revendedores:
  - Cadastrar novo:
  -
- Registro de compras:
  - Cadastrar nova compra:
  - Listar compras
- Autenticação JWT:
  - Obter token:
  - Atualizar token:
  - Enviar token:
- Testes:
  - Unitários:
  - Integracionais:

# Conclusão
Funcionamento em geral(escolha de bibliotecas), extenções, correções, trajeto para o futuro, dificuldades (REST)...
