import psycopg2
import csv
import boto3

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

        # Verificar se a consulta retornou resultados (se a tabela existir)
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




host = "localhost"
database = "geotabadapterdb"
user = "geotabadapter_client"
password = "spfc929305"
tabela = "ChargeEvents"
coluna_data = "StartTime"  
arquivo_csv = "ChargeEvents_full.csv"

extrair_e_exportar_para_csv(host, database, user, password, tabela, coluna_data, arquivo_csv)

arquivo_envio ='Dashboard_new.csv'
s3_key = "Raw/" f'{arquivo_envio}' 
bucket_name = 'telemetriaeventos'


def envio_S3(csv, bucket_name, s3_key):
  access_key_id = "ASIAVAHJXYLT5Z5W627M"
  secret_access_key = "/S9oRm1AHQWbdZPDDA0rWUzf8wMsN8tj67cSH5n/"
  aws_session_token = "IQoJb3JpZ2luX2VjEEkaCXVzLXdlc3QtMiJIMEYCIQDNXmti0EkAMG9zTWQ6VuB/CTfxos/B/FC/ao2DIWlLLQIhAJ/YK09QUOMzXjBgV0G+iNiVDlYGVhY9VpfHkMdRHXjlKr4CCJL//////////wEQAhoMMzQ0MDg3NTc3MzE5IgykBmdmEIVhG68ugpQqkgIVqLK9rZU4JhjKQMV93oD7Y5DaDmcVlLtcY1KXwNnfBesb62Y8SffWjYnw8t+8TWtFuza6uOPqzke127vEeEE7n+NEEZyGkjhXvZAufu09CNWS66+FmKLmKWIcX0k/uMqU24SX5zXhfikIhGx+22+a6aaoCbg0eY11NJh/0oRPX8/yEXgK6+VaAhyHm2L91yfwHfZ3GQSQ4gmwP43wq710ALs6ULSjUKN1T19Tph705fmsAteTzrgvfbWLZHTL+HKRzo9CiopT/b7WUbuAb8XgSZ6VsT6CoIbbJ8h59/4Z+FtD+/HUVquN2AStFQAHlIygIxvEi4lPOXh9xVUfUHKNDS2ZWspo04zj1bvo13j7gq0yMJ/N8LcGOpwBOxZIU22JbupXx1a+keovCg622jPfKze4MOtxL8nd8GouBn9+mrToyaPUcZVA4SbeVO/+l+zq7uvYBndBVv8+7q3jq3I6nqzHZVSTdOPW7ox9rlLtYv4EIPA2kuMVQdAwBQeEZwWaarMXsD4FM0OcGeCa5LEyX9DBUVSApeDud2fCF9zLBq9VuXT0M7xZ288rMSxzr0FwVz7/1ABS"
  s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token = aws_session_token
    )

  with open(csv, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, s3_key)
        print(f"Arquivo {csv} enviado para s3://{bucket_name}/{s3_key}")


envio_S3(arquivo_envio,bucket_name,s3_key)