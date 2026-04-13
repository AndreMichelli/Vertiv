import pandas as pd, time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# marcas = "Vertiv , VORAGO"
# caminhoBase = "C:/Bots/Lista de preços"
data_coleta = datetime.today().strftime("%Y-%m-%d")

dados = []
# parametros = [marcas, caminhoBase]
def buscar_produtos(parametros):
    try:
        marcas = parametros[0]
        marcas = marcas.split(",")
        caminhoBase = parametros[1]
        escrever_log("PYTHON", "Marcas: " + str(marcas), caminhoBase)
        escrever_log("PYTHON", "caminhoBase: " + str(caminhoBase), caminhoBase)
        caminhoCSV = caminhoBase + "/csv_pcel.csv"
        urlBase = "https://www.pcel.com/"
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage') 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        escrever_log("PYTHON", "Iniciando a extração dos dados", caminhoBase)
        for marca in marcas:
            pagina = 1
            proxPag = True
            while proxPag == True:
                marca_url = marca.lower().strip().replace(" ", "-")
                url = f"{urlBase}{marca_url}?page={pagina}"
                driver.get(url)
                time.sleep(2)  # pequeno delay para evitar carregamento incompleto

                items = driver.find_elements(By.CLASS_NAME, "product-description-row")
                if not items:
                    escrever_log("PYTHON", "Pagina vazia: " + url, caminhoBase)
                    proxPag = False
                else:
                    for item in items:
                        try:
                            nome = item.find_element(By.CLASS_NAME, "product-description-text").find_element(By.TAG_NAME, "h5").text
                        except:
                            nome = "-"
                        
                        try:
                            sku = item.find_element(By.CLASS_NAME, "model-list").get_attribute("innerText").split(" ")[1]
                        except:
                            sku = "-"

                        try:
                            linkProduto = item.find_element(By.CLASS_NAME, "product-description-text").find_element(By.TAG_NAME, "a").get_attribute("href").strip()
                        except:
                            linkProduto = "-"

                        try:
                            preco = item.find_element(By.CLASS_NAME, "price").text.strip().replace(" ", "").replace("$", "").replace(",", "")
                        except:
                            preco = "-"

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
                            "disponiveis": "-",
                            "sku": sku
                        })
                pagina += 1
        driver.quit()
        df = pd.DataFrame(dados)
        df.to_csv(caminhoCSV, index=False, encoding="utf-8-sig", header=False)
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