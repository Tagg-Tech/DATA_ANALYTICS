
import psutil # Captura os dados da maquina
import pandas as pd # Usamos duas funções, uma para transformar em DataFrame e outra para agrupar
import time # Responsavel pela discretização de tempo
import mysql.connector 




conn = mysql.connector.connect( #Estabelecendo conexao com o banco de dados
        host="localhost",
        user="root",
        password="Lqsym@2020",
        database="TagTech"
    )


cursor = conn.cursor() #Criando um cursor (objeto que executa códigos)

query = f"""SELECT * FROM registros;"""

 
cursor.execute(query) # Executando select 


resultado = cursor.fetchall()

print(resultado)

print(type(resultado))

column_names = ['idRegistro', 'gigaBytesMemoria', 'percMemoria', 'qtdUtilizadaDisco', 'percDisco', 'percCPU', 'freqCPU', 'dataHora']

df = pd.DataFrame(resultado, columns=column_names)
print(df)

df.to_csv('registros.csv', index=False)