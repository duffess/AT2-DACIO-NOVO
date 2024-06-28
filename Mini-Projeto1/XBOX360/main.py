import requests
from bs4 import BeautifulSoup
import pandas as pd

url_xbox360 = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Xbox_360"

try:
    response = requests.get(url_xbox360)
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
        data[0][4:5] = ['_'.join((data[0][4], i)) for i in data[1]]

        df = pd.DataFrame(data, columns=data[0])
        if not df.empty:
            df.columns = df.iloc[0]
            df = df[2:]
            # df.columns = [f"col_{i}" for i in range(len(df.columns))]  # Renomeia as colunas
            df = df.dropna(how='all')
            df.reset_index(drop=True, inplace=True)
            df = df.drop_duplicates()
            df.fillna('VALOR-VAZIO', inplace=True)

            dirCSV = "../AT2/Mini-Projeto1/XBOX360/dataframeXBOX360.csv"
            df.to_csv(dirCSV, encoding='utf-8', index=False)

            dirJSON = "../AT2/Mini-Projeto1/XBOX360/dataframeXBOX360.json"
            df.to_json(dirJSON, index=False)

            dirXLSX = "../AT2/Mini-Projeto1/XBOX360/dataframeXBOX360.xlsx"
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
