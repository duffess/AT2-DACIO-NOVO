import requests
from bs4 import BeautifulSoup
import pandas as pd

url_xbox_series = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Xbox_Series_X_e_Series_S"

try:
    response = requests.get(url_xbox_series)
    response.raise_for_status()  # Lança uma exceção se a requisição não for bem-sucedida (código de status diferente de 2xx)
    
    conteudo = response.content.decode("utf-8")
    soup = BeautifulSoup(conteudo, 'html.parser')

    table = soup.find('table', {'class': 'sortable'})

    if table:
        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [cell.get_text(strip=True) for cell in cols]
            data.append(cols)

        df = pd.DataFrame(data)
        if not df.empty:
            df.columns = df.iloc[0]
            df = df[1:]
            df = df.dropna(how='all')
            df.reset_index(drop=True, inplace=True)
            df = df.drop_duplicates()
            df.fillna('VALOR-VAZIO', inplace=True)

            dirCSV = "../AT2/Mini-Projeto1/XBOXxs/dataframeXBOXSERIES.csv"
            df.to_csv(dirCSV, encoding='utf-8', index=False)

            dirJSON = "../AT2/Mini-Projeto1/XBOXxs/dataframeXBOXSERIES.json"
            df.to_json(dirJSON, index=False)

            dirXLSX = "../AT2/Mini-Projeto1/XBOXxs/dataframeXBOXSERIES.xlsx"
            df.to_excel(dirXLSX, index=False)

            print(df)
        else:
            print('DataFrame vazio - nenhuma tabela de jogos encontrada')
    else:
        print('Tabela não encontrada')
except requests.exceptions.RequestException as e:
    print(f'Erro durante a requisição HTTP: {e}')
except Exception as e:
    print(f'Ocorreu um erro inesperado: {e}')
