import pandas as pd  # importa o pandas
import sqlite3  # importa o sqlite3
import requests  # importa o requests

# Conectar-se ao banco de dados para ler a tabela AllGames
try:
    conn = sqlite3.connect('../AT2/Mini-Projeto3/games.db')  # conecta ao banco de dados SQLite
    df = pd.read_sql_query('SELECT * FROM AllGames', conn)  # lê a tabela AllGames do banco de dados
except (sqlite3.Error, pd.io.sql.DatabaseError) as e:
    print(f"Erro ao conectar ou ler o banco de dados: {e}")
    df = pd.DataFrame()  # cria um DataFrame vazio como fallback
finally:
    if conn:
        conn.close()  # fecha a conexão

# Lista que contenha todos os jogos relatados no banco de dados
all_games = df['game_name'].tolist() if not df.empty else []  # converte a coluna 'game_name' em uma lista

# Função para consultar a API do Mercado Livre e extrair informações
def consultar_api_mercado_livre(jogo):
    try:
        url = f'https://api.mercadolibre.com/sites/MLB/search?category=MLB186456&q={jogo}'  # define a URL da API do Mercado Livre
        response = requests.get(url)  # faz uma requisição HTTP GET para a URL
        response.raise_for_status()  # verifica se a resposta foi bem-sucedida (status 200)
        resultados = response.json().get('results', [])  # obtém os resultados da resposta JSON
        jogos = []  # cria uma lista vazia para armazenar os dados dos jogos
        for item in resultados:  # para cada item nos resultados
            jogos.append({
                'name': item.get('title'),  # obtém o título do item
                'price': item.get('price'),  # obtém o preço do item
                'permalink': item.get('permalink')  # obtém o link do item
            })
        return jogos  # retorna a lista de jogos
    except requests.RequestException as e:
        print(f"Erro ao consultar a API do Mercado Livre para o jogo '{jogo}': {e}")
        return []  # retorna uma lista vazia se a requisição falhar

# Consultar a API do Mercado Livre para cada jogo e armazenar os dados em uma lista
dados_jogos = []  # cria uma lista vazia para armazenar os dados dos jogos
for jogo in all_games:  # para cada jogo na lista all_games
    info_jogos = consultar_api_mercado_livre(jogo)  # consulta a API do Mercado Livre para o jogo
    dados_jogos.extend(info_jogos)  # adiciona os dados dos jogos à lista dados_jogos

# Criar DataFrame com os dados dos jogos
dados_jogos_df = pd.DataFrame(dados_jogos)  # cria um DataFrame com os dados dos jogos

# Conectar-se ao novo banco de dados para salvar os dados extraídos da API
try:
    conn_ml = sqlite3.connect('../AT2/Mini-Projeto4/jogos_do_ML.db')  # conecta ao novo banco de dados SQLite
    cursor_ml = conn_ml.cursor()  # cria um cursor para executar comandos SQL

    # Criar tabela no novo banco de dados
    cursor_ml.execute('''
        CREATE TABLE IF NOT EXISTS JogosDoML (
           name TEXT,
           price REAL,
           permalink TEXT
        )
    ''')  # cria a tabela JogosDoML se não existir

    # Salvar os dados extraídos no novo banco de dados
    dados_jogos_df.to_sql('JogosDoML', conn_ml, if_exists='replace', index=False)  # insere os dados na tabela JogosDoML
except sqlite3.Error as e:
    print(f"Erro ao conectar ou manipular o banco de dados: {e}")
finally:
    if conn_ml:
        conn_ml.close()  # fecha a conexão

# Verificar se os dados foram inseridos corretamente
try:
    conn_ml = sqlite3.connect('../AT2/Mini-Projeto4/jogos_do_ML.db')  # reconecta ao banco de dados SQLite
    cursor_ml = conn_ml.cursor()  # cria um cursor para executar comandos SQL

    # Consultar dados da tabela JogosDoML
    cursor_ml.execute("SELECT name FROM sqlite_master WHERE type='table';")  # consulta os nomes das tabelas no banco de dados
    tables = cursor_ml.fetchall()  # obtém os nomes das tabelas

    # Consultar dados das tabelas existentes
    tables_data = {}  # cria um dicionário vazio para armazenar os dados das tabelas
    for table in tables:  # para cada tabela
        table_name = table[0]  # obtém o nome da tabela
        cursor_ml.execute(f"SELECT * FROM {table_name}")  # consulta todos os dados da tabela
        tables_data[table_name] = cursor_ml.fetchall()  # armazena os dados da tabela no dicionário
except sqlite3.Error as e:
    print(f"Erro ao consultar dados do banco de dados: {e}")
finally:
    if conn_ml:
        conn_ml.close()  # fecha a conexão

# print(tables_data)  # imprime os dados das tabelas (comentado para nao pesar o terminal)
