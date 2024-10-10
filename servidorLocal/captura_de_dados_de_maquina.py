import psutil, time, mysql.connector, platform, pandas as pd,  dotenv , os, requests,  json
from socket import gethostname
dotenv.load_dotenv(dotenv.find_dotenv())
senhaBD = os.getenv("SENHA_DB")

i = 0
nomeMaquina = gethostname()  
sistemaOperacional = platform.system()



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


while True:

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
    
    usoDeCPU = 87
    if usoDeCPU >= 80:      mandarAlertaJira("CPU", usoDeCPU)
    if percentRAM >= 80:    mandarAlertaJira("memória RAM", percentRAM)
    if percentDisco >= 80:  mandarAlertaJira("disco", percentDisco)
    
    
    
    
    i = i + 1

    sql = "INSERT INTO registros ( percentualMemoria, qtdUtilizadaDisco, percentualDisco, percentualCPU, frequenciaCPU) VALUES (%s, %s, %s, %s, %s)"
    values = (percentRAM, discoUsado, percentDisco, usoDeCPU, freqDeCPU)
    cursor.execute(sql, values)
    db_connection.commit()

    time.sleep(10)

    
    print("##############################################################################################")