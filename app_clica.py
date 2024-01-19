from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import urllib.parse
import requests
from credentials_tlgram_bot import *

def extract_Jobs_Gupy():
    termo = 'Analista de Suporte'
    remoto = 'only-remote'
    vaga = urllib.parse.quote(termo)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    options = Options()
    options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(options=options) as driver:
        url = f"https://portal.gupy.io/job-search/Working={remoto}&term={vaga}&remoteWorking={remoto}"
        driver.get(url)
        print(url)
        time.sleep(5)

        # Realizar o scroll até o final da página
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Busca todos os elementos do xpath dos cards da pagina
        card_elements = driver.find_elements('xpath', './/*[@id="__next"]/div[3]/div/div/main/ul/li')
        # Busca por todos os links da pagina separando-o por card
        links = driver.find_elements('xpath', '//*[@id="__next"]/div[3]/div/div/main/ul/li/div/a')
        # Fiz o laço de for para capturar todos os dados
        for index, card_element in enumerate(card_elements):

            company = card_element.find_element('xpath', './/*[@class="sc-efBctP dpAAMR sc-70b75bd4-5 dCVCel"]').text
            job = card_element.find_element('xpath', './/*[@class="sc-llJcti bGqDEZ sc-70b75bd4-7 ftHylk"]').text
            data_pub = card_element.find_element('xpath', './div/a/div/p[3]').text.split()
            #print(data_pub) #Verifica em quantas partes está quebrada a informação e se está separada por , ou ;
            data_pub = data_pub[3].strip()
            #print(data_pub)
            local_vaga = card_element.find_element('xpath', './div/a/div/p[1]').text
            # # Fazer tratativa se houve ou não exibir o que houver
            tip_trab = card_element.find_element('xpath', './div/a/div/p[2]').text
            # print(local_vaga) #Verifica em quantas partes está quebrada a informação e se está separada por , ou ;
            # print(tip_trab)

            link = links[index].get_attribute('href')
            time.sleep(3)

            print("Empresa: ", company)
            print("Vaga: ", job)
            print("Data da Publicação: ", data_pub)
            print("Local da vaga: ", local_vaga)
            print("tipo Trabalho: ", tip_trab)
            print("Links", link)
            print("---")
            hoje = f"Data da Extração de Vagas: {now}"
            print(hoje)

            # cria uma lista com os dados coletados formatados em forma de string
            messages = ""
            message = f"Empresa: {company}\n"
            message += f"Vaga: {job}\n"
            message += f"Data da Publicação: {data_pub}\n"
            message += f"local: {local_vaga}\n"
            message += f"local: {tip_trab}\n"
            message += f"Link: {link}\n"
            message += "=" * 30 + "\n\n"

            # Enviando ao Telegram
            url = f'https://api.telegram.org/bot{token_bot}/sendMessage?chat_id={chat_group}&text={message}+{hoje}'
            requests.get(url, verify=True)


    driver.quit()

#def extract_Jobs_Linkedin():


if __name__ == "__main__":
    extract_Jobs_Gupy()
    #extract_Jobs_Linkedin()