# Drivers para abrir o navegador
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options

# Localizar dentro do html
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

# BS4
from bs4 import BeautifulSoup

# Pandas 
import pandas as pd 

# Time -> Controlar o tempo de espera
import time

def page_driver(driver): 
    """
    Retorna o HTML da página
    """

    page_content = driver.page_source
    html_page = BeautifulSoup(page_content, 'html.parser')
    return html_page

def acesso(path: str, url: str, usuario: str, senha: str):
    """
    Função de acesso ao Blob Storage
    """

    # Configurando o Driver do Selenium 
    service = Service(path)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    driver.get(url)

    # Acesso o Blob Storage
    driver.find_element(By.ID, "i0116").send_keys(usuario)
    driver.find_element(By.ID, "i0116").send_keys(Keys.ENTER)

    driver.find_element(By.ID, "i0118").send_keys(senha)
    time.sleep(3)
    driver.find_element(By.ID, "i0118").send_keys(Keys.ENTER)

    print("Acesso realizado com sucesso!")

    return driver

def click_LoadMore(driver) -> None:
    """
    Função que clica em "Load More"
    """

    botao = driver.find_element(By.CLASS_NAME, "azc-grid-pageable-loadMoreLabel")
    if botao.text == "Load more":
        botao.click()
        time.sleep(10) # tempo para a página compilar as informações 
        return "OK"
    else: 
        return None
    
def save_infos(html_page) -> None:
    """
    Salva as informações coletadas do Blob Storage em um csv
    """

    nomes = ""
    status = ""

    # Itera sobre cada "conteiner" as informações dos arquivos
    rows = html_page.find_all('tr', {'role': 'row'})
    for row in rows: 
        # Encontra todas as informações de cada arquivo e armazena em uma lista
        elements = row.find_all('td', {'role': 'gridcell'})
        elements = [elements.text for element in elements]

        # Realiza a limpeza dos dados e concatena em uma string
        if (len(elements) > 0) and (elements[0] != "[..]") and (elements[0] != "No results"): 
            nome_arquivo = elements[0]
            nomes = nomes + "," + nome_arquivo
            status_arquivo = elements[2]
            status = status + "," + status_arquivo.rstrip()
    
    # Salva as informações em um arquivo CSV
    df = pd.DataFrame(data={'nome_arquivo': nomes.split(',')[1:], 'status': status.split(',')[1:]})
    df.to_csv('./data/cold_files_mainframe.csv', index= False)