from datetime import datetime
import mysql.connector
import csv


def inserir_dados_csv(param):
    try:
        # host, port, user, senha, banco, csv_path = param
        log_path = param[0]
        csv_path = param[1]
        escrever_log("PYTHON", "Parametros" + str(param), log_path)
        escrever_log("PYTHON", "arquivo csv -> " + csv_path, log_path)
        conexao = mysql.connector.connect(
            host="amerpsapweb01.ext.vertivco.com",
            port="3306",
            user="competitors_price",
            password="eeamcVW@R8!34",
            database="vertivweb"
        )
        # conexao = mysql.connector.connect(
        #     host=host,
        #     port=port,
        #     user=user,
        #     password=senha,
        #     database=banco
        # )
        cursor = conexao.cursor()

        query = """
        INSERT INTO competitors_price (
            product, price_slip, price_pix, price_installment,
            maximum_installments, collection_date, department, website,
            source, currency, quantity, sku, created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, now(), now()
        )
        """

        with open(csv_path, mode='r', encoding='utf-8') as arquivo_csv:
            leitor = csv.reader(arquivo_csv, delimiter=";")
            for linha in leitor:
                # escrever_log("PYTHON", "linha atual -> " +
                #              str(linha), log_path)
                # escrever_log(
                #     "PYTHON", "comprimento da linha atual -> " + str(len(linha)), log_path)
                if not linha or len(linha) < 12:
                    continue

                linha = [None if (valor.strip() == "-" or valor.strip()
                                  == "") else valor.strip() for valor in linha]
                if linha[5]:
                    linha[5] = converter_data(linha[5], log_path)
                else:
                    print("linha com erro na conversão da data: " + linha[5])
                    continue

                # formatando os valores para o padrão do banco
                for i in [1, 2, 3, 4]:
                    linha[i] = formatar_valor(linha[i])
                cursor.execute(query, linha)

        conexao.commit()
        print("Inserção concluída com sucesso.")
        return "Insert finalizado"

    except Exception as e:
        escrever_log("PYTHON", "Erro: " + str(e), log_path)
        return "Erro no insert: " + str(e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()


def converter_data(data_str, log_path):
    try:
        data_str = data_str.strip()
        if not data_str or data_str == "-":
            return None

        # Se já estiver no formato yyyy-mm-dd, retorna sem alterar
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return data_str
        except ValueError:
            pass

        # Caso contrário, tenta converter de dd/mm/yyyy
        try:
            data_convertida = datetime.strptime(data_str, "%d/%m/%Y")
            return data_convertida.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Formato de data inválido: {data_str}")
    except Exception as e:
        escrever_log("PYTHON", "Erro: " + str(e), log_path)
        return None


def formatar_valor(valor):
    if not valor or valor.strip() in ("-", ""):
        return None

    valor = valor.strip()

    # Encontrar o último ponto ou vírgula
    ultima_virgula = valor.rfind(',')
    ultimo_ponto = valor.rfind('.')
    ultimo_sep = max(ultima_virgula, ultimo_ponto)

    if ultimo_sep == -1:
        # Nenhum separador, só converte direto
        try:
            return float(valor)
        except ValueError:
            return None

    # Separador decimal
    decimal = valor[ultimo_sep]

    # Parte inteira: remove todos os outros separadores
    parte_inteira = valor[:ultimo_sep].replace('.', '').replace(',', '')
    parte_decimal = valor[ultimo_sep+1:]

    # ponto como decimal
    valor_normalizado = f"{parte_inteira}.{parte_decimal}"
    try:
        return float(valor_normalizado)
    except ValueError:
        return None


def escrever_log(nivel, mensagem, caminhoArquivo):
    agora = datetime.now()
    caminhoArquivo = caminhoArquivo + "/log.txt"
    data = agora.strftime("%d-%m-%Y")
    hora = agora.strftime("%H_%M_%S")
    linha = f"{data} - {hora} - [{nivel.upper()}] - {mensagem}\n"

    with open(caminhoArquivo, "a", encoding="utf-8") as f:
        f.write(linha)

# param = ["amerpsapweb01.ext.vertivco.com", "3306", "competitors_price",
#          "eeamcVW@R8!34", "vertivweb", "C:/Bots/Lista de preços/teste.csv"]
# param = "C:/Bots/Lista de preços/teste.csv"
# param = ["C:/Bots/Lista de preços", "C:/Bots/Lista de preços/csv_aux.csv"]
# inserir_dados_csv(param)
