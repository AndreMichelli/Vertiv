import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# marcas = "CYBERPOWER , VORAGO"
# marcas = 'CYBERPOWER, VICA OPTIMA, VORAGO, SMARTBITT, FORZA, SCHNEIDER ELECTRIC, EPCOM, CDP, KOBLENZ, EATON, SMS, INTELBRAS, RAGTECH, NHS, DELTA, VERTIV, CSB, HPE, TRIPP LITE, APC'
# caminhoBase = "C:/Bots/Lista de preços"
data_coleta = datetime.today().strftime("%Y-%m-%d")

# Lista para armazenar os dados
dados = []
# parametros = [marcas, caminhoBase]


def buscar_produtos(parametros):
    try:
        marcas = parametros[0]
        marcas = marcas.split(",")
        caminhoBase = parametros[1]
        # escrever_log("PYTHON", "Marcas: " + str(marcas), caminhoBase)
        # escrever_log("PYTHON", "caminhoBase: " + str(caminhoBase), caminhoBase)
        caminhoCSV = caminhoBase + "/csv_intercompras.csv"
        urlBase = "https://intercompras.com/marcas/"
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        escrever_log("PYTHON", "Iniciando a extração dos dados", caminhoBase)
        for marca in marcas:
            pagina = 1
            proxPag = True
            while proxPag == True:
                marca_url = marca.lower().strip().replace(" ", "-")
                url = f"{urlBase}{marca_url}?page={pagina}"
                driver.get(url)
                # pequeno delay para evitar carregamento incompleto
                time.sleep(2)

                items = driver.find_elements(
                    By.CLASS_NAME, "divContentProductInfo")
                print("--> items: " + str(items))

                if not items:
                    escrever_log("PYTHON", "Pagina vazia: " + url, caminhoBase)
                    proxPag = False
                else:
                    for item in items:
                        try:
                            nome = item.find_element(
                                By.CLASS_NAME, "spanProductListInfoTitle").get_attribute("innerText")
                        except:
                            nome = "-"

                        try:
                            linkProduto = item.find_element(
                                By.CLASS_NAME, "spanProductListInfoTitle").get_attribute("href")
                        except:
                            linkProduto = "-"

                        try:
                            preco = item.find_element(By.CLASS_NAME, "divProductListPrice").get_attribute(
                                "innerText").replace("$", "")
                        except:
                            preco = "-"

                        try:
                            disponiveis = item.find_element(
                                By.CLASS_NAME, "available").get_attribute("innerText")
                        except:
                            disponiveis = "-"
                        print("dados capturados")
                        escrever_log("PYTHON", "--> incluindo dados no dicionario", caminhoBase)

                        # Salvar no dicionário
                        dados.append({
                            "nome": nome,
                            "preco": preco,
                            "preco_pix": "-",
                            "preco_parecela": "-",
                            "qtd_parcela": "-",
                            "data": data_coleta,
                            "departamento": marca,
                            "site": urlBase,
                            "fonte": linkProduto,
                            "moeda": "MXN",
                            "disponiveis": disponiveis,
                            "sku": "-"
                        })
                pagina += 1
        escrever_log("PYTHON", "--> dicionario: " + str(dados), caminhoBase)
        driver.quit()
        df = pd.DataFrame(dados)
        df.to_csv(caminhoCSV, index=False, encoding="utf-8-sig", header=False)
        escrever_log("PYTHON", "Finalizando a extração dos dados", caminhoBase)
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
# buscar_produtos(parametros)
# print("Arquivo CSV salvo com sucesso.")
