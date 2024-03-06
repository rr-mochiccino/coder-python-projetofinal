# Projeto Final do Curso de Python - CoderHouse

Bem-vindo ao repositório do projeto final do curso de Python da CoderHouse. Este README fornecerá uma visão geral do projeto e detalhará a estrutura do projeto.Este README fornece uma explicação do código em Python para extrair, transformar e carregar (ETL) dados Pokémon da PokeAPI para um banco de dados SQLite. O código está dividido em várias funções, cada uma com um propósito específico. O processo envolve a extração de dados da PokeAPI, a transformação em DataFrames estruturados, a exploração e limpeza dos dados, e, finalmente, o armazenamento em um banco de dados SQLite.

## Sumário

1. [Extração de Dados da PokeAPI](#extração-de-dados-da-pokeapi)
2. [Criação de DataFrames](#criação-de-dataframes)
3. [Execução de Tarefas da API](#execução-de-tarefas-da-api)
4. [Alerta de Notificação](#alerta-de-notificação)
5. [Extração de Dados da API e Criação de DataFrames](#extração-de-dados-da-api-e-criação-de-dataframes)
6. [Transformação de Dados](#transformação-de-dados)
7. [Impressão de Informações dos DataFrames](#impressão-de-informações-dos-dataframes)
8. [Operações de Banco de Dados](#operações-de-banco-de-dados)
9. [Testes](#testes)

## Extração de Dados da PokeAPI

A função `extrai_api_data` é responsável por fazer requisições à PokeAPI. Ela recupera dados da API iterativamente, lidando com erros e interrupções adequadamente.

## Criação de DataFrames

A função `cria_dataframe` é uma função utilitária para criar um DataFrame a partir de um dicionário fornecido. Ela serve como um passo fundamental na organização dos dados extraídos.

## Execução de Tarefas da API

A função `executa_tarefa_api` é projetada para ser usada com a biblioteca `schedule`, executando tarefas em intervalos agendados. Ela chama a função `extrai_api_data` e retorna o resultado.

## Alerta de Notificação

A função `alerta` cria alertas de notificação com base nos níveis de alerta, nomes de bases, etapas e erros especificados. Ela utiliza a biblioteca `notification` para exibir alertas.

## Extração de Dados da API e Criação de DataFrames

A função `extracao_criacao_df` combina a extração de dados da PokeAPI e a criação de DataFrames. Ela diferencia entre URLs de Pokémon, habilidades e tipos e lida com erros adequadamente.

## Transformação de Dados

A função `transformando_dados` realiza transformações nos DataFrames, incluindo tratamento de valores ausentes, renomeação de colunas e explosão de listas em linhas separadas.

## Impressão de Informações dos DataFrames

A função `imprime_info_df` imprime informações sobre os DataFrames, incluindo tipos de colunas, contagens não nulas e cabeçalhos dos DataFrames.

## Operações de Banco de Dados

A função `salva_tabela_banco` salva um DataFrame em uma tabela de banco de dados SQLite, substituindo a tabela existente se ela já existir. A função `carrega_banco` carrega um DataFrame do banco de dados.

## Testes

O código conclui com a extração de dados brutos da PokeAPI, a transformação de dados, a impressão de informações dos DataFrames e o salvamento dos DataFrames transformados no banco de dados SQLite. O exemplo fornecido envolve dados de Pokémon, habilidades e tipos.















# Configuração do Ambiente Virtual

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto. Siga as etapas abaixo para configurar e ativar o ambiente virtual.

## Instalação do Virtualenv (se ainda não estiver instalado)

1. Abra um terminal e execute o seguinte comando para instalar o `virtualenv` no Windows:

```bash
pip install virtualenv
````

2 . Navegue até o diretório do projeto:

```bash
cd caminho/do/seu/projeto
```

3. Crie um ambiente virtual:
   
```bash
virtualenv vvenv
```

4. Ativação do Ambiente Virtual

No Windows (cmd):
```bash
venv\Scripts\activate
```
No Windows (PowerShell):
```bash
.\venv\Scripts\Activate
```

5. Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências usando o seguinte comando:
```bash
pip install -r requirements.txt
```
Agora você está pronto para executar o código dentro do ambiente virtual isolado!



