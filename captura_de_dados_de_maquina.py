import psutil
import time
import mysql.connector
import platform
from socket import gethostname

i = 0
nomeMaquina = gethostname()  
sistemaOperacional = platform.system()

db_connection = mysql.connector.connect(host='localhost', user='root', password='18082005vmag@', database='TagTech')
cursor = db_connection.cursor()


while True:

    if(sistemaOperacional=="Windows"):
        usoDeDisco = psutil.disk_usage('C:\\')
    elif(sistemaOperacional=="Linux"):
        usoDeDisco = psutil.disk_usage('/')

    usoDeCPU = psutil.cpu_percent(interval=1)
    freqDeCPU = psutil.cpu_freq()
    usoDeMemo = psutil.virtual_memory()


    i = i + 1

    sql = "INSERT INTO registros ( percentualMemoria, qtdUtilizadaDisco, percentualDisco, percentualCPU, frequenciaCPU) VALUES (%s, %s, %s, %s, %s)"
    values = (usoDeMemo.percent, usoDeDisco.used, usoDeDisco.percent, usoDeCPU, freqDeCPU.current)
    cursor.execute(sql, values)
    db_connection.commit()
    print(freqDeCPU)

    print(
    """
    {:d}º CAPTURA
    ----------------------------------

    Percentual de uso de CPU: {:.2f}%
    Frequência da CPU: {:.2f} MHz

    Quantidade total de memória: {:.2f} GB
    Percentual de uso da memória: {:.2f}%

    Quantidade utilizada de disco: {:.2f} GB
    Percentual de uso do disco: {:.2f}%

    """
    .format(i, usoDeCPU, freqDeCPU.current, 
               usoDeMemo.percent, 
               round(usoDeDisco.used / (1024 ** 3),2),  # Formatado como float com 2 casas decimais
               usoDeDisco.percent))
    time.sleep(10)

    
    print("##############################################################################################")