
import psutil, dotenv , os, requests,  json, mysql.connector
import time
import platform
from socket import gethostname
import pandas as pd
from datetime import datetime, timedelta

dotenv.load_dotenv(dotenv.find_dotenv())
senhaBD = os.getenv("SENHA_DB")
i=0
nomeMaquina = gethostname()
print(nomeMaquina)  
sistemaOperacional = platform.system()
print('antes do banco')
print('passando pro banco',flush=True)
db_connection = mysql.connector.connect(
    host='localhost', user='gaspa', password=senhaBD, database='TagTech',port=3306,ssl_disabled = True # Host = ip da EC2
    )
cursor = db_connection.cursor()

baseurl = os.getenv("URL")
url = f'{baseurl}//rest/api/2/issue'
token = os.getenv("TOKEN")
email = os.getenv("LOGIN")



ultimoChamadoCPU = datetime.now() - timedelta(hours=1)
ultimoChamadoRAM = datetime.now() - timedelta(hours=1)
ultimoChamadoDisco = datetime.now() - timedelta(hours=1)


print(ultimoChamadoRAM)





def mandarAlertaJira(componente, numPico):
    data = pd.Timestamp.now()
    data = data.replace(microsecond=0)
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }


    payload=json.dumps(
        {
            "fields":{
                "project":
                    {
                        "key":"TTCS"
                    },
                    "summary": "pico de uso do componente : {} as {}".format(componente, data),
                    "description": "O componente {} teve um pico de uso de ´´{} por cento as **{} no servidor ''{}".format(componente,numPico, data, nomeMaquina),
                    "issuetype":{
                        "name":"Support"
                    }
            }
        }
    )



    response = requests.post(url,headers=headers,data=payload,auth=(email,token))


    print(response.text)


def capturarDf():
    global ultimoChamadoCPU, ultimoChamadoRAM, ultimoChamadoDisco  
    
    
    print("entrou")
    column_names = ['idDados', 'dataHora', 'percCPU', 'tempoInativo', 'percRAM', 'gigaBytesRAM', 'percDisc', 'usedDisc', 'fkNotebook']

    df = pd.DataFrame(columns=column_names)
    i = 0

    
    while i < 5:
        print("loop",  i)
    # Criar o DataFrame vazio com as colunas definidas

        if(sistemaOperacional=="Windows"):
            disco = psutil.disk_usage('C:\\')
        elif(sistemaOperacional=="Linux"):
            disco = psutil.disk_usage('/')
        usoDeCPU = psutil.cpu_percent(interval=1)
        freqDeCPU = psutil.cpu_freq()
        freqDeCPU = freqDeCPU.current
        
        memRAM = psutil.virtual_memory()
        ramGigaBytes = memRAM.used / 1024 ** 3
        percentRAM = memRAM.percent 
        discoUsado = disco.used
        percentDisco = disco.percent
        
        sql_select = "SELECT alertaCPU,alertaRAM,alertaDISCO FROM maquina WHERE placaDeRede = %s"
        values_select = (nomeMaquina,)    
        cursor.execute(sql_select,values_select)
        result = cursor.fetchone()
        
        
        hora_atual = datetime.now()
        if usoDeCPU >= result[0] and hora_atual - ultimoChamadoCPU >= timedelta(hours=1): 
            mandarAlertaJira("CPU", usoDeCPU)
            ultimoChamadoCPU = hora_atual
        if percentRAM >= result[1] and hora_atual - ultimoChamadoRAM >= timedelta(hours=1):
            mandarAlertaJira("memória RAM", percentRAM)
            ultimoChamadoRAM = hora_atual
        if percentDisco >= result[2] and hora_atual - ultimoChamadoDisco >= timedelta(hours=1):
            mandarAlertaJira("disco", percentDisco)
            ultimoChamadoDisco = hora_atual
        
    
        i = i + 1

        values = (percentRAM, ramGigaBytes, discoUsado, percentDisco, usoDeCPU, freqDeCPU)
        data = pd.Timestamp.now()
        data_formatada = data.strftime('%Y-%m-%d_%H-%M-%S')
        print(data_formatada)
        dados = {
        'idDados': i,
        'dataHora': data_formatada,
        'percCPU': freqDeCPU,
        'tempoInativo': freqDeCPU,
        'percRAM': percentRAM,
        'gigaBytesRAM': ramGigaBytes,
        'percDisc': percentDisco,
        'usedDisc': discoUsado,
        'fkNotebook': nomeMaquina
    }

    sql_select = "SELECT idMaquina FROM maquina WHERE placaDeRede = %s"
    values_select = (nomeMaquina,)    
    cursor.execute(sql_select,values_select)
    result = cursor.fetchone()
    
    if result:
        id_maquina = result[0]


        sql = "INSERT INTO registros ( percentualMemoria, gigaBytesMemoria, qtdUtilizadaDisco, percentualDisco, percentualCPU, frequenciaCPU, fkMaquina) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (percentRAM, ramGigaBytes, discoUsado, percentDisco, usoDeCPU, freqDeCPU, id_maquina)
        cursor.execute(sql, values)
        db_connection.commit()
    else:
        print("Não há nenhuma maquina com este hostname")
        
        
    novo_df = pd.DataFrame([dados])

    # Concatenar os dados ao DataFrame original
    df = pd.concat([df, novo_df], ignore_index=True)

    print(df)

    
    print(freqDeCPU)

    time.sleep(5)

        
    print("##############################################################################################")
        
    df.to_csv(f'ec2Producao_Atual/csv/{data_formatada}.csv', index=False)
    
    
while True:
    print("rodando")
    capturarDf()