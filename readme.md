# Sample Scraping
O projeto tem como proposito ser uma simples demonstracao da utilizacao de
selenium para validar CPFs gerados aleatoriamente em sites de terceiros.

## Funcionamento
Para simular uma situacao real, foram criadas duas aplicacoes distintas que se
comunicam atraves de uma fila RabbitMQ e uma base de dados MongoDB.

O publisherapp tem a responsabilidade de: Gerar uma string de 11 digitos para
ser um possivel CPF; Verifica se esse CPF ja existe na base de dados e, caso
nao, adiciona esse CPF para uma fila que posteriormente sera processada.

O botapp tem como responsabilidade: receber de uma fila valores de CPF,
verificar em sites de terceiros se o CPF e valido ou nao, e, por fim, registrar
no banco de dados o resultado da consulta.

### Execucao do projeto
Docker e docker-compose sao requisitos para execucao do projeto. Para
executa-lo, clone o repositorio e no diretorio de destino, digite:

```
docker-compose up --build
```


## TODO LIST
- melhorar documentacao com diagramas e esquemas explicativos;
- usar image docker selenium-hub e demais imagens selenium-node  para
possibilitar outros navegadores;
    - refatorar codigo: usar pattern abstract factory para possibilitar combinar
      navegadores diferentes com sites diferentes no modulo cpf_validator;
- refatorar codigo: remover magic-numbers
