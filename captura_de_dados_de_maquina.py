import psutil
import time
import mysql.connector
import platform
from socket import gethostname

i = 0
nomeMaquina = gethostname()
sistemaOperacional = platform.system()

# db_connection = mysql.connector.connect(host='host', user='usuario', password='senha', database='testeAutomacao')
# cursor = db_connection.cursor()


while True:

    if(sistemaOperacional=="Windows"):
        UsoDeDisco = psutil.disk_usage('C:\\')
    elif(sistemaOperacional=="Linux"):
        UsoDeDisco = psutil.disk_usage('/')

    UsoDeCPU = psutil.cpu_percent(interval=1)
    FreqDeCPU = psutil.cpu_freq()
    UsoDeMemo = psutil.virtual_memory()

    qtdNucleos = psutil.cpu_count()
    qtdNucleosVirtuais = psutil.cpu_count(logical=False)

    i = i + 1

    # sql = "INSERT INTO registros (percentualCPU, usoCPU, usoMemoria, usoDisco, qtdNucleos, qtdNucleosVirtuais, nomeMaquina) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # values = (FreqDeCPU.current, UsoDeCPU, UsoDeMemo.percent, UsoDeDisco.percent, qtdNucleos, qtdNucleosVirtuais, nomeMaquina)
    # cursor.execute(sql, values)
    # db_connection.commit()

    print(
    """
    {:d}º CAPTURA
    ----------------------------------
    Quantidade total de núcleos de CPU: {:d}
    Quantidade total de núcleos virtuais de CPU: {:d}
    Percentual de uso de CPU: {:.2f}%
    Frequência da CPU: {:.2f} MHz

    Quantidade total de memória: {:d}
    Percentual de uso da memória: {:.2f}%

    Quantidade total de disco: {:d}
    Quantidade utilizada de disco: {:d}
    Percentual de uso do disco: {:.2f}%

    Nome da máquina: {:s}
    Sistema Operacional: {:s}

    """.format(i, qtdNucleos, qtdNucleosVirtuais, UsoDeCPU, FreqDeCPU.current, 
               UsoDeMemo.total, UsoDeMemo.percent, 
               UsoDeDisco.total, UsoDeDisco.used, UsoDeDisco.percent, 
               nomeMaquina, sistemaOperacional))
    time.sleep(3)


    
