from utils.funcoes import page_driver, acesso, click_LoadMore, save_infos
import json
import time

def main(driver):
    print("Navegar até a pasta desejada!")

    time.sleep(30)

    # Listando todos os arquivos possíveis na pasta
    while True: 
        if click_LoadMore(driver) != "OK":
            break
    
    print("Salvando as informações em um arquivo .csv")

    html_page = page_driver(driver)
    save_infos(html_page)

    # Finalizando o Driver
    driver.quit()
    

if __name__ == "__main__":
    json_file = json.load(open('./utils/variables.json'))
    path = json_file['path_driver']
    url = json_file['url']
    usuario = json_file['usuario']
    senha = json_file['senha']

    driver = acesso(path, url, usuario, senha)
    main(driver)