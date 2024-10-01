import psycopg2
import csv

def extrair_e_exportar_para_csv(host, database, user, password, tabela, coluna_data, arquivo_csv):
    try:
        # Conexão com o banco de dados
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        # Criar um cursor para executar comandos SQL
        cur = conn.cursor()

        # Construir a consulta SQL \
        query = """ 
            SELECT
            SUBSTRING(device."Name", STRPOS(device."Name", '|') + 2) as "ModeloCarro",
            charge.*
            FROM public."ChargeEvents" as charge
            LEFT JOIN public."Devices" as device
            ON charge."DeviceId" = device."GeotabId"
            ORDER BY 
            charge."StartTime" DESC;
        """

        # Executar a consulta
        cur.execute(query)

        # Verificar se a consulta retornou resultados (i.e., se a tabela existe)
        if cur.rowcount > 0:
            # Obter os resultados
            resultados = cur.fetchall()

            # Abrir o arquivo CSV para escrita
            with open(arquivo_csv, 'w', newline='') as csvfile:
                # Criar um objeto escritor CSV
                writer = csv.writer(csvfile)

                # Escrever o cabeçalho (nomes das colunas)
                writer.writerow([desc[0] for desc in cur.description])

                # Escrever as linhas de dados
                writer.writerows(resultados)
        else:
            print(f"Tabela '{tabela}' não encontrada no banco de dados.")

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao banco de dados ou escrever no arquivo CSV:", error)

    finally:
        # Fechar a conexão e o arquivo CSV
        if conn:
            cur.close()
            conn.close()



# Exemplo de uso:
host = "localhost"
database = "geotabadapterdb"
user = "geotabadapter_client"
password = "spfc929305"
tabela = "ChargeEvents"
coluna_data = "StartTime"  # Substitua pelo nome da sua coluna de data
arquivo_csv = "ChargeEvents_full"

extrair_e_exportar_para_csv(host, database, user, password, tabela, coluna_data, arquivo_csv)
