# Sample Scraping
O projeto tem como proposito ser uma simples demonstracao da utilizacao de
selenium para validar CPFs gerados aleatoriamente em sites de terceiros.

## Funcionamento
Para simular uma situacao real, foram criadas duas aplicacoes distintas.

O publisherapp tem a responsabilidade de: Gerar uma string de 11 digitos para
ser um possivel CPF; Verifica se esse CPF ja existe na base de dados e, caso
nao, adiciona esse CPF para uma fila que posteriormente sera processada.

O botapp tem como responsabilidade: receber de uma fila valores de CPF,
verificar em sites de terceiros se o CPF e valido ou nao, e, por fim, registrar
no banco de dados o resultado da consulta.

## TODO LIST
- melhorar documentacao com diagramas e esquemas explicativos.
