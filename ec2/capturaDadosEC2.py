
import psutil, dotenv , os, requests,  json
import time
import platform
from socket import gethostname
import pandas as pd

dotenv.load_dotenv(dotenv.find_dotenv())

nomeMaquina = gethostname()  
sistemaOperacional = platform.system()


baseurl = os.getenv("URL")
url = f'{baseurl}//rest/api/2/issue'
token = os.getenv("TOKEN")
email = os.getenv("LOGIN")




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
                        "key":"TAG"
                    },
                    "summary": "pico de uso do componente : {} as {}".format(componente, data),
                    "description": "O componente {} teve um pico de uso de {} por cento as {} no servidor {}".format(componente,numPico, data, nomeMaquina),
                    "issuetype":{
                        "name":"Support"
                    }
            }
        }
    )



    response = requests.post(url,headers=headers,data=payload,auth=(email,token))


    print(response.text)

    


def capturarDf():
    column_names = ['idDados', 'dataHora', 'percCPU', 'tempoInativo', 'percRAM', 'gigaBytesRAM', 'percDisc', 'usedDisc', 'fkNotebook']

    df = pd.DataFrame(columns=column_names)
    i = 0

    while i < 5:

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
        
        
        if usoDeCPU >= 80:      mandarAlertaJira("CPU", usoDeCPU)
        if percentRAM >= 80:    mandarAlertaJira("memória RAM", percentRAM)
        if percentDisco >= 80:  mandarAlertaJira("disco", percentDisco)

        i = i + 1

        values = (percentRAM, ramGigaBytes, discoUsado, percentDisco, usoDeCPU, freqDeCPU)
        data = pd.Timestamp.now()
        data_formatada = data.strftime('%Y-%m-%d_%H-%M-%S')
        dados = {
        'idDados': i,
        'dataHora': data,
        'percCPU': freqDeCPU,
        'tempoInativo': freqDeCPU,
        'percRAM': percentRAM,
        'gigaBytesRAM': ramGigaBytes,
        'percDisc': percentDisco,
        'usedDisc': discoUsado,
        'fkNotebook': 101
    }
        
        
        
        novo_df = pd.DataFrame([dados])

    # Concatenar os dados ao DataFrame original
        df = pd.concat([df, novo_df], ignore_index=True)

        print(df)

    
        print(freqDeCPU)

        time.sleep(1)

        
        print("##############################################################################################")
        
    df.to_csv(f'csv/{data_formatada}.csv', index=False)
    
    
while True:
    capturarDf()