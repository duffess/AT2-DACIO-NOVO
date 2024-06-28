import pandas as pd  # importa o pandas
import sqlite3  # importa o sqlite3

# Carregar o arquivo Excel consolidado em um DataFrame
try:
    df = pd.read_excel('../AT2/Mini-Projeto2/dados-excel.xlsx')  # lê o arquivo Excel
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")
    df = pd.DataFrame()
    # cria um DataFrame vazio como fallback

# Separar os jogos que estão concatenados
if not df.empty:
    df['jogos_preferidos'] = df['jogos_preferidos'].str.split('|')  # divide a string de jogos preferidos em uma lista
# Função para encontrar interseção de jogos preferidos entre todos os usuários

def jogos_comuns(df):
    jogos_interseccao = set.intersection(*df['jogos_preferidos'].apply(set)); # converte a lista de jogos preferidos do df em um set ( o * 'eh usado para desempacotara lista recebida')
    return jogos_interseccao #


def todos_jogos(df):
    jogos_uniao = set.union(*df['jogos_preferidos'].apply(set)); #
    return jogos_uniao



def jogos_unicos(df):
    # Criar um conjunto com todos os jogos mencionados
    todos_jogos_set = set()
    for jogos_lista in df['jogos_preferidos']:
        todos_jogos_set.update(jogos_lista)
    
    # Contar quantas vezes cada jogo aparece
    contagem_jogos = {}
    for jogos_lista in df['jogos_preferidos']:
        for jogo in jogos_lista:
            if jogo in contagem_jogos:
                contagem_jogos[jogo] += 1
            else:
                contagem_jogos[jogo] = 1
    
    # Encontrar jogos mencionados apenas uma vez
    jogos_unicos = {jogo for jogo, count in contagem_jogos.items() if count == 1}
    
    return jogos_unicos

# Aplicar as funções
if not df.empty:
    try:
        jogos_comuns_set = jogos_comuns(df)  # aplica a função jogos_comuns
        todos_jogos_set = todos_jogos(df)  # aplica a função todos_jogos
        jogos_unicos_list = jogos_unicos(df)  # aplica a função jogos_unicos

        # Adicionar jogos únicos ao DataFrame
        df['jogos_unicos'] = jogos_unicos_list  # adiciona a lista de jogos únicos ao DataFrame
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Exibir resultados
if not df.empty:
    print("Jogos comuns entre todos os usuários:")
    print(jogos_comuns_set)  # imprime os jogos comuns

    print("\nTodos os jogos preferidos (união):")
    print(todos_jogos_set)  # imprime todos os jogos preferidos

    print("\nJogos únicos por usuário:")

# Para a tabela AllGames
if not df.empty:
    all_games = set(game for games in df['jogos_preferidos'] for game in games)  # cria um conjunto de todos os jogos

# Para a tabela UniqueGames
    game_counts = {}  # cria um dicionário para contar a ocorrência de cada jogo
    for games in df['jogos_preferidos']:  # para cada lista de jogos
        for game in games:  # para cada jogo na lista
            if game in game_counts:  # se o jogo já está no dicionário
                game_counts[game] += 1  # incrementa a contagem
            else:  # se o jogo não está no dicionário
                game_counts[game] = 1  # adiciona o jogo ao dicionário com contagem 1
    unique_games = set(game for game, count in game_counts.items() if count == 1)  # cria um conjunto de jogos únicos (aparecem apenas uma vez)

# Para a tabela ImportantGames
    important_games = pd.Series(game_counts).sort_values(ascending=False)  # cria uma série com os jogos e suas contagens, ordenada de forma decrescente

# Conectar-se ao banco de dados
try:
    conn = sqlite3.connect('../AT2/Mini-Projeto3/games.db')  # conecta ao banco de dados SQLite
    cursor = conn.cursor()  # cria um cursor para executar comandos SQL

    # Criar tabelas no banco de dados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AllGames (
           game_name text primary key
        )
    ''')  # cria a tabela AllGames se não existir

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UniqueGames (
           game_name text primary key
        )
    ''')  # cria a tabela UniqueGames se não existir

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ImportantGames (
           game_name text primary key,
           aparicoes integer
        )
    ''')  # cria a tabela ImportantGames se não existir

    # Inserir dados na tabela AllGames
    all_games_df = pd.DataFrame(list(all_games), columns=['game_name'])  # cria um DataFrame com todos os jogos
    all_games_df.to_sql('AllGames', conn, if_exists='replace', index=False)  # insere os dados na tabela AllGames

    # Inserir dados na tabela UniqueGames
    unique_games_df = pd.DataFrame(list(unique_games), columns=['game_name'])  # cria um DataFrame com os jogos únicos
    unique_games_df.to_sql('UniqueGames', conn, if_exists='replace', index=False)  # insere os dados na tabela UniqueGames

    # Inserir dados na tabela ImportantGames
    important_games_df = important_games.reset_index()  # reseta o índice do DataFrame
    important_games_df.columns = ['game_name', 'aparicoes']  # define os nomes das colunas
    important_games_df.to_sql('ImportantGames', conn, if_exists='replace', index=False)  # insere os dados na tabela ImportantGames
except sqlite3.Error as e:
    print(f"Erro ao conectar ou manipular o banco de dados: {e}")
    conn.rollback()  # desfaz as alterações caso haja um erro
finally:
    if 'conn' in locals() and conn:
        conn.close()  # fecha a conexão

