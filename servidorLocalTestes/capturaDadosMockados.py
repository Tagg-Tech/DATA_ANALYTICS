import psutil, time, mysql.connector, platform, pandas as pd,  dotenv , os, requests,  json
from socket import gethostname
import random
from datetime import timedelta
dotenv.load_dotenv(dotenv.find_dotenv())
senhaBD = os.getenv("SENHA_DB")

i = 0
nomeMaquina = gethostname()  
sistemaOperacional = platform.system()

dataHora = pd.Timestamp('2024-09-12 19:39:51')


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
                    "description": "O componente {} teve um pico de uso de {} por cento as {} no servidor {}".format(componente,numPico, dataHora, nomeMaquina),
                    "issuetype":{
                        "name":"Support"
                    }
            }
        }
    )



    response = requests.post(url,headers=headers,data=payload,auth=(email,token))


    print(response.text)




estaEmPico = 'nao'


percentCPU = [32,68,14]
percentRAM = [67,61,49]
percentDisco = [12,59, 37]
discoUsado = [453863952384, 253863952384, 333863952384]
freqDeCPU = [2200.00, 2200.00, 2200.00]

while True:


    if estaEmPico == 'nao':
        
        
        entrarDisco = random.randint(1,15)
        
        if(entrarDisco == 1):
            qualDisco = random.randint(1,3)
            aumentoDisco = round(random.uniform(0.1, 0.6),2)
            if qualDisco == 1:
                percentDisco[0] += aumentoDisco
                
            elif qualDisco == 2:
                percentDisco[1] += aumentoDisco
            else:
                percentDisco[2] += aumentoDisco
                
                
            
            
            cont = 0
            while cont < (len(percentCPU)) - 1:
                percentRAM += round((random.uniform(-4,4)),2)
                percentCPU += round((random.uniform(-4,4)),2)

        
    
    
    
        numAleatorio = random.randint(1,500)
        if numAleatorio >= 42 and numAleatorio <= 50:
            print('Entrou em estado de explosão')
            computadorEmPico = random.randint(0,2)
            numAleatorioComponente = random.randint(1,2)
            porcentExplosao = (random.randint(8,16)) + 80
            estaEmPico = 'explosao'
            tempoForaDoAr = random.randint(2,6)
            estaForaDoAr = False
            
            if numAleatorioComponente == 1:
                percentCPU = porcentExplosao
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
                percentCPU = porcentExplosao
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
            percentCPU = 0
            freqDeCPU = 0   
            tempoForaDoAr -= 1
        elif componenteExplosao == 'cpu':
            if estaEmPico == 'explosao': percentCPU += random.randint(7,9)
            if estaEmPico == 'crescente':percentCPU += random.randint(3,5)
            
            if percentCPU > 100:
                estaForaDoAr = True
                percentRAM = 0
                discoUsado = 0
                percentDisco = 0
                percentCPU = 0
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
                percentCPU = 0
                freqDeCPU = 0   
                tempoForaDoAr -= 1
            else:
                percentCPU = psutil.cpu_percent(interval=1)
                freqDeCPU = psutil.cpu_freq()
                freqDeCPU = freqDeCPU.current
                discoUsado = disco.used
                percentDisco = disco.percent
    
            
            
            
            

    
    # if percentCPU >= 80:      mandarAlertaJira("CPU", percentCPU)
    # if percentRAM >= 80:    mandarAlertaJira("memória RAM", percentRAM)
    # if percentDisco >= 80:  mandarAlertaJira("disco", percentDisco)
    
    
    
    
    
    
    
    
    i = i + 1

    sql = "INSERT INTO registros ( percentualMemoria, qtdUtilizadaDisco, percentualDisco, percentualCPU, frequenciaCPU, dataHora) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (percentRAM, discoUsado, percentDisco, percentCPU, freqDeCPU, dataHora)
    cursor.execute(sql, values)
    db_connection.commit()

    dataHora += timedelta(minutes=5)

    time.sleep(3)
    
    

    
    print("##############################################################################################")