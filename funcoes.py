import pandas as pd
import requests
import schedule
import time
from plyer import notification
from datetime import datetime
import sqlite3

def extrai_api_data(api_url: str) -> list:
    ''' 
    Extrai dados da API pela quantidade de
    páginas. Assim que uma página sem conteúdo é 
    encontrada, a função para. 
    Enquanto a função está sendo executada, ela 
    pega os dados da página em formato json e coloca
    em uma lista.

    Parametros
    ----------
    api_url : str
            url da página

    Retorna
    -------
    lista_url : list
        lista com o json de cada página

    '''
    
    lista_url = []
    i = 1

    while True:
        url = f"{api_url}/{i}/"
        response = requests.get(url)

        if response.status_code == 200:
            data_json = response.json()
            lista_url.append(data_json)
            i += 1
        else:
            print(f"Página {i}: Erro ao acessar a API")
            break

    return lista_url


def cria_dataframe(dicio: dict) -> pd.DataFrame:
    '''
    Cria um dataframe baseado em um dicionário e
    um index baseado na coluna que o usuário define.
    
    Parametros
    ----------
    dicio : dict
        dicionário com dados para o dataframe

    Retorna
    -------
    df : dataframe
        dataframe criado
    '''
    
    df = pd.DataFrame(dicio)
    
    return df

def executa_tarefa_api(api_url: str) -> list:
    ''' 
    Executa uma função como o objetivo de ser utilizada
    na schedule 
    
    Parametros
    ----------
    api_url : str 
            url da api
    Retorna
    -------
    resultado : list 
            lista de paginas extraidas da funcao extrai_api_data
    '''
    
    print("Executando a tarefa")
    resultado = extrai_api_data(api_url)
    return resultado

def alerta(nivel:int, base:str, etapa:str, erro:str):
    '''
    Cria uma notificação usando o notification
    baseada no nível do alerta, o nome da base
    e etapa providenciadas pelo usuário.
    Adiciona também a data e hora que a notificação
    aconteceu.
    
    Parametros:
    ----------
    nivel : int
            nivel do alerta
    base : str 
            nome da base
    etapa : str
            etapa que aconteceu
    erro : str
            erro ocorrido
    '''
    
    try:
        nome_alerta = ''

        if nivel == 1:
            nome_alerta = "Baixo"
        elif nivel == 2:
            nome_alerta = "Médio"
        else:
            nome_alerta = "Alto"
        
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        notification.notify(
            title=f"ATENÇÃO: Alerta {nome_alerta}",
            message=f"Falha no carregamento da base {base} na etapa {etapa},\
            \nErro: {erro}\
            \n{current_date_time}",
            app_name="Python",
            timeout=10
        )
        
    except Exception as error:
        print(f"Erro detectado:{error}")
        
        
def extracao_criacao_df(url:str)-> pd.DataFrame:
    '''
    Extrai a data de uma api e baseada no tipo 
    da url, extrai diferentemente as listas e 
    cria em um dataframe 

    Parametros:
    ----------
    url : str
            url da api

    Retorna
    -------
    df : dataframe
        a data extraida em formato dataframe
    '''
    
    #extrai a url
    
    
    if "pokemon" in url:
        print(f"{20*'-'} POKÉMON {20*'-'}")
    elif "ability" in url:
        print(f"{20*'-'} HABILIDADE {20*'-'}")
    elif "type" in url:
        print(f"{20*'-'} TIPO {20*'-'}")
    

    
    try:
        try:
            lista_url = executa_tarefa_api(url)

            schedule.every(1).hours.do(executa_tarefa_api, url)

            while True:
                schedule.run_pending()
                time.sleep(1)
                break

        except Exception as erro:
            alerta(1, "Pokemon" if "pokemon" in url else ("Habilidades" if "ability" in url else "Tipo"), "Extração_API", erro)

        if "pokemon" in url:
            #cria as listas com as caracteristicas
            lista_pokemon_id = [pokemon["id"] for pokemon in lista_url]
            lista_pokemon_nome = [pokemon["name"] for pokemon in lista_url]
            lista_habilidades = [[ability["ability"]["name"] for ability in pokemon["abilities"]] for pokemon in lista_url]
            lista_exp_base = [pokemon["base_experience"] for pokemon in lista_url]
            lista_tipo = [[ability["type"]["name"] for ability in pokemon["types"]] for pokemon in lista_url]
            lista_altura =[pokemon["height"] for pokemon in lista_url]
            lista_peso = [pokemon["weight"] for pokemon in lista_url]

            #cria um dicionario com as listas
            dicio = {"id":lista_pokemon_id,
            "nome": lista_pokemon_nome,
            "habilidade" : lista_habilidades,
            "exp_base": lista_exp_base,
            "tipo": lista_tipo,
            "altura": lista_altura,
            "peso": lista_peso}

            df = cria_dataframe(dicio)
                
        elif "ability" in url:
            #cria as listas com as caracteristicas
            lista_tipos_id = [tipo["id"] for tipo in lista_url]
            lista_tipos_nome = [tipo["name"] for tipo in lista_url]
            lista_geracao = [tipo["generation"]["name"] for tipo in lista_url]
            lista_pokemon = [[poke["pokemon"]["name"] for poke in pokemon["pokemon"]] for pokemon in lista_url]
            
            #cria um dicionario com as listas
            dicio = {"id":lista_tipos_id,
            "nome": lista_tipos_nome,
            "geracao": lista_geracao,
            "pokemons": lista_pokemon,
            }


            df = cria_dataframe(dicio)
            

            
        elif "type" in url:
            #cria as listas com as caracteristicas
            lista_tipos_id = [tipo["id"] for tipo in lista_url]
            lista_tipos_nome = [tipo["name"] for tipo in lista_url]
            lista_geracao = [tipo["generation"]["name"] for tipo in lista_url]
            lista_pokemon = [[poke["pokemon"]["name"] for poke in pokemon["pokemon"]] for pokemon in lista_url]

            #cria um dicionario com as listas
            dicio = {"id":lista_tipos_id,
            "nome": lista_tipos_nome,
            "geracao": lista_geracao,
            "pokemons": lista_pokemon,
            }
            


            df = cria_dataframe(dicio)

        return df
    
    except Exception as erro:
        alerta(3,"APIs", "Extração", erro)
        
        
def transformando_dados(df: pd.DataFrame, nome: list) -> pd.DataFrame:
    '''
    Transforma os dados de um dataframe, seja preenchendo 
    os dados faltantes, seja renomeando as colunas ou seja
    transformando uma lista de dados em dados separados. 

    Parametros:
    ----------
    df : dataframe
            dataframe a ser transformado
    nome: list
            lista dos nomes dos dataframes

    Retorna
    -------
    df : dataframe
            dataframe transformado
    '''
    
    
    if nome == "pokemon":
        try:
            df_new = df.copy()
            #preencher os dados vazios com 0
            df_new["exp_base"] = df_new["exp_base"].fillna(0)
            # transformar uma lista em linhas diferentes
            df_new = df_new.explode('habilidade', ignore_index=True)
            df_new = df_new.explode('tipo', ignore_index=True)
            #renomear a coluna id
            df_new.rename(columns={"id": "id_pokemon"}, inplace=True)
        except Exception as erro:
            alerta(3, "Tipo", "Transformação", erro)
    elif nome == "tipo":
        try:
            df_new = df.copy()
            # transformar uma lista em linhas diferentes
            df_new = df_new.explode('pokemons', ignore_index=True)
            #renomear a coluna id e pokemons
            df_new.rename(columns={"pokemons": "pokemon"}, inplace=True)
            df_new.rename(columns={"id": "id_tipo"}, inplace=True)

        except Exception as erro:
            alerta(3, "Tipo", "Transformação", erro)
    elif nome == "habilidade":
        try:
            df_new = df.copy()
            # transformar uma lista em linhas diferentes
            df_new = df_new.explode('pokemons', ignore_index=True)
            #renomear a coluna id e pokemons
            df_new.rename(columns={"pokemons": "pokemon"}, inplace=True)
            df_new.rename(columns={"id": "id_habilidade"}, inplace=True)
            #deletar a linha que não tem uma habilidade existente 
            df_new.drop(index=2937, inplace=True)
        except Exception as erro:
            alerta(3, "Tipo", "Transformação", erro)
    
    else:
        print("NOME DE DATAFRAME NÃO EXISTE")
    
    return df_new


def imprime_info_df(dfs:list, nome_dfs:list):
    '''
    Imprime as informações (info) e o cabeçalho (head) 
    do dataframe. 

    Parametros:
    ----------
    dfs : list
            lista dos dataframes a serem impressos
    nome_dfs : list
            lista de nomes dos dataframes
    
    '''
    
    print(f"-----INFORMAÇÕES-------\n")
    for i,df in enumerate(dfs):
        print(f"-----{nome_dfs[i]}-------")
        print(df.info())
    
    print(f"-----CABEÇALHOS-------\n")
    for i,df in enumerate(dfs):
        print(f"-----{nome_dfs[i]}-------")
        print(df.head())
        
        
def salva_tabela_banco(df: pd.DataFrame ,nome_tabela: str) -> bool:
    '''
    Salva o dataframe no banco de dados. 

    Parametros:
    ----------
    df : dataframe
            dataframe a ser inserido no banco
    nome_tabela : str
            nome da tabela no banco de dados
    
    '''
    
    conn = sqlite3.connect("coderhouse.db")
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela}")
    conn.commit()
    df.to_sql(nome_tabela, conn, if_exists = "replace", index=False)
    conn.close()
    
    return True 

def carrega_banco(nome_tabela: str) -> pd.DataFrame:
    '''
    Carrega o dataframe do banco de dados. 

    Parametros:
    ----------
    nome_tabela : str
            nome da tabela no banco de dados
    Retorna
    -------
    df : dataframe
            dataframe da tabela do banco de dados
    
    '''
    conn = sqlite3.connect("coderhouse.db")
    query = f"SELECT * FROM {nome_tabela}"
    df = pd.read_sql(query, conn)
    
    return df