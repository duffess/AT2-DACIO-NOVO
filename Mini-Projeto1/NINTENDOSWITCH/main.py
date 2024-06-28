import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_Nintendo_Switch"

try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    all_tables = soup.find_all('table', {'class': 'sortable'})
    combined_data = []

    for table in all_tables:
        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [cell.get_text(strip=True) for cell in cols]
            data.append(cols)
        combined_data.extend(data)

    if combined_data:
        df = pd.DataFrame(combined_data)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.dropna(how='all')
        df.reset_index(drop=True, inplace=True)
        df = df.drop_duplicates()
        df.fillna('VALOR-VAZIO', inplace=True)
        df.head();
        df.info();
        dirCSV = "../AT2/Mini-Projeto1/NINTENDOSWITCH/dataframeNINTENDOSWITCH.csv"
        df.to_csv(dirCSV, encoding='utf-8', index=False)

        dirJSON = "../AT2/Mini-Projeto1/NINTENDOSWITCH/dataframeNINTENDOSWITCH.json"
        df.to_json(dirJSON, index=False)

        dirXLSX = "../AT2/Mini-Projeto1/NINTENDOSWITCH/dataframeNINTENDOSWITCH.xlsx"
        df.to_excel(dirXLSX, index=False)

        print("Dados combinados salvos com sucesso.")
    else:
        print("Nenhuma tabela encontrada.")

except requests.exceptions.RequestException as e:
    print(f'Erro durante a requisição HTTP: {e}')
except Exception as e:
    print(f'Ocorreu um erro inesperado: {e}')
