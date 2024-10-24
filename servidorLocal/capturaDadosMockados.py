import psutil, time, mysql.connector, platform, pandas as pd,  dotenv , os, requests,  json
from socket import gethostname
import random
from datetime import timedelta
dotenv.load_dotenv(dotenv.find_dotenv())
senhaBD = os.getenv("SENHA_DB")

i = 0
nomeMaquina = gethostname()  
sistemaOperacional = platform.system()

dataHora = pd.Timestamp('2024-09-28 19:39:51')


db_connection = mysql.connector.connect(
    host='localhost', user='root', password=senhaBD, database='TagTech'
    )
cursor = db_connection.cursor()



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
                        "key":"THD"
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




estaEmPico = 'nao'

while True:


    if estaEmPico == 'nao':
        
        
                
        if(sistemaOperacional=="Windows"):
            disco = psutil.disk_usage('C:\\')
        elif(sistemaOperacional=="Linux"):
            disco = psutil.disk_usage('/')
                

        usoDeCPU = psutil.cpu_percent(interval=1)
        freqDeCPU = psutil.cpu_freq()
        freqDeCPU = freqDeCPU.current
        
        memRAM = psutil.virtual_memory()
        percentRAM = memRAM.percent 
        discoUsado = disco.used
        percentDisco = disco.percent
    
    
    

        
    
    
    
        numAleatorio = random.randint(1,500)
        if numAleatorio >= 42 and numAleatorio <= 50:
            print('Entrou em estado de explosão')
            numAleatorioComponente = random.randint(1,2)
            porcentExplosao = (random.randint(8,16)) + 80
            estaEmPico = 'explosao'
            tempoForaDoAr = random.randint(2,6)
            estaForaDoAr = False
            
            if numAleatorioComponente == 1:
                usoDeCPU = porcentExplosao
                componenteExplosao = 'cpu'
            else:
                percentRAM = porcentExplosao
                componenteExplosao = 'ram'
                
        elif numAleatorio >= 100 and numAleatorio <= 120:
            estaForaDoAr = False
            print('Entrou em estado de pico')
            numAleatorioComponente = random.randint(1,2)
            porcentExplosao = (random.randint(8,20)) + 68
            estaEmPico = 'crescente'
            tempoForaDoAr = 0
            tempoForaDoAr = random.randint(1,4)
            
            
            
            
            if numAleatorioComponente == 1:
                usoDeCPU = porcentExplosao
                componenteExplosao = 'cpu'
            else:
                percentRAM = porcentExplosao
                componenteExplosao = 'ram'
            
    elif estaEmPico == 'explosao' or estaEmPico == 'crescente':
        if tempoForaDoAr == 0: 
            estaEmPico = 'nao'
            estaForaDoAr = False
        elif estaForaDoAr == True:
            percentRAM = 0
            discoUsado = 0
            percentDisco = 0
            usoDeCPU = 0
            freqDeCPU = 0   
            tempoForaDoAr -= 1
        elif componenteExplosao == 'cpu':
            if estaEmPico == 'explosao': usoDeCPU += random.randint(7,9)
            if estaEmPico == 'crescente':usoDeCPU += random.randint(3,5)
            
            if usoDeCPU > 100:
                estaForaDoAr = True
                percentRAM = 0
                discoUsado = 0
                percentDisco = 0
                usoDeCPU = 0
                freqDeCPU = 0   
                tempoForaDoAr -= 1
            else:
                freqDeCPU = psutil.cpu_freq()
                freqDeCPU = freqDeCPU.current
                memRAM = psutil.virtual_memory()
                percentRAM = memRAM.percent 
                discoUsado = disco.used
                percentDisco = disco.percent
                
            
        elif componenteExplosao == 'ram':
            if estaEmPico == 'explosao': percentRAM += random.randint(5,9)
            if estaEmPico == 'crescente':percentRAM += random.randint(3,6)
            
            
            if percentRAM > 100:
                estaForaDoAr = True
                percentRAM = 0
                discoUsado = 0
                percentDisco = 0
                usoDeCPU = 0
                freqDeCPU = 0   
                tempoForaDoAr -= 1
            else:
                usoDeCPU = psutil.cpu_percent(interval=1)
                freqDeCPU = psutil.cpu_freq()
                freqDeCPU = freqDeCPU.current
                discoUsado = disco.used
                percentDisco = disco.percent
    
            
            
            
            

    
    # if usoDeCPU >= 80:      mandarAlertaJira("CPU", usoDeCPU)
    # if percentRAM >= 80:    mandarAlertaJira("memória RAM", percentRAM)
    # if percentDisco >= 80:  mandarAlertaJira("disco", percentDisco)
    
    
    
    
    
    
    
    
    i = i + 1

    sql = "INSERT INTO registros ( percentualMemoria, qtdUtilizadaDisco, percentualDisco, percentualCPU, frequenciaCPU, dataHora) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (percentRAM, discoUsado, percentDisco, usoDeCPU, freqDeCPU, dataHora)
    cursor.execute(sql, values)
    db_connection.commit()

    dataHora += timedelta(minutes=10)

    time.sleep(3)
    
    

    
    print("##############################################################################################")