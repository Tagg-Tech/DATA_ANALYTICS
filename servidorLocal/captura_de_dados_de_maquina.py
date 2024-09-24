import psutil
import time
import mysql.connector
import platform
from socket import gethostname
import pandas as pd

i = 0
nomeMaquina = gethostname()  
sistemaOperacional = platform.system()

db_connection = mysql.connector.connect(
    host='localhost', user='root', password='Lqsym@2020', database='TagTech'
    )
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

    time.sleep(10)

    
    print("##############################################################################################")