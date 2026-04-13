import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

links = "https://www.abasteo.mx/Energia/Proteccion-Contra-Descargas/No-Break-UPS/No-Break-UPS/,https://www.abasteo.mx/Energia/Proteccion-Contra-Descargas/No-Break-UPS/Baterias-para-No-Break/,https://www.abasteo.mx/Energia/PDU-s/,https://www.abasteo.mx/Energia/Baterias/Gabinetes-para-Baterias/,https://www.abasteo.mx/Energia/Baterias/Baterias-Selladas/"

caminhoBase = "C:/Bots/Lista de preços"
data_coleta = datetime.today().strftime("%Y-%m-%d")

dados = []
parametros = [links, caminhoBase]


def buscar_produtos(parametros):
    try:
        links = parametros[0]
        links = links.split(",")
        caminhoBase = parametros[1]
        escrever_log("PYTHON", "links: " + str(links), caminhoBase)
        escrever_log("PYTHON", "caminhoBase: " + str(caminhoBase), caminhoBase)
        caminhoCSV = caminhoBase + "/csv_abasteo.csv"
        urlBase = "https://www.abasteo.mx"
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        escrever_log("PYTHON", "Iniciando a extração dos dados", caminhoBase)
        for link in links:
            pagina = 1
            proxPag = True
            while proxPag == True:
                url = f"{link}{pagina}/"
                driver.get(url)
                # pequeno delay para evitar carregamento incompleto
                grid_produtos = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "c-product-list"))
                )
                items = grid_produtos.find_elements(By.CLASS_NAME, "cell")
                escrever_log("PYTHON", "grid da pagina: " +
                             str(grid_produtos), caminhoBase)
                items = grid_produtos.find_elements(By.CLASS_NAME, "cell")
                escrever_log("PYTHON", "itens da pagina: " +
                             str(items), caminhoBase)
                if not items:
                    escrever_log("PYTHON", "Pagina vazia: " + url, caminhoBase)
                    proxPag = False
                # else:
                    # for item in items:
                    # try:
                    #     nome = item.find_element(
                    #         By.CLASS_NAME, "product-description-text").find_element(By.TAG_NAME, "h5").text
                    # except:
                    #     nome = "-"

                    # try:
                    #     sku = item.find_element(
                    #         By.CLASS_NAME, "model-list").get_attribute("innerText").split(" ")[1]
                    # except:
                    #     sku = "-"

                    # try:
                    #     linkProduto = item.find_element(
                    #         By.CLASS_NAME, "product-description-text").find_element(By.TAG_NAME, "a").get_attribute("href").strip()
                    # except:
                    #     linkProduto = "-"

                    # try:
                    #     preco = item.find_element(By.CLASS_NAME, "price").text.strip().replace(
                    #         " ", "").replace("$", "").replace(",", "")
                    # except:
                    #     preco = "-"

                    # # Salvar no dicionário
                    # dados.append({
                    #     "nome": nome,
                    #     "preco": preco,
                    #     "preco_pix": "-",
                    #     "preco_parecela": "-",
                    #     "qtd_parcela": "-",
                    #     "data": data_coleta,
                    #     "departamento": marca,
                    #     "site": urlBase,
                    #     "fonte": linkProduto,
                    #     "moeda": "MXN",
                    #     "disponiveis": "-",
                    #     "sku": sku
                    # })
                    # pagina += 1
        # driver.quit()
        # df = pd.DataFrame(dados)
        # df.to_csv(caminhoCSV, index=False, encoding="utf-8-sig", header=False)
        return caminhoCSV
    except Exception as e:
        escrever_log("PYTHON", "Erro: " + str(e), caminhoBase)
        return "Erro python: " + str(e)


def escrever_log(nivel, mensagem, caminhoArquivo):
    agora = datetime.now()
    caminhoArquivo = caminhoArquivo + "/log.txt"
    data = agora.strftime("%d-%m-%Y")
    hora = agora.strftime("%H_%M_%S")
    linha = f"{data} - {hora} - [{nivel.upper()}] - {mensagem}\n"

    with open(caminhoArquivo, "a", encoding="utf-8") as f:
        f.write(linha)


# Rodar busca
buscar_produtos(parametros)
print("Arquivo CSV salvo com sucesso.")
