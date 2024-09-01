import psutil
import time
# import mysql.connector
import platform
from socket import gethostname

i = 0
nomeMaquina = gethostname()
sistemaOperacional = platform.system()

# db_connection = mysql.connector.connect(host='host', user='usuario', password='senha', database='testeAutomacao')
# cursor = db_connection.cursor()


while True:

    if(sistemaOperacional=="Windows"):
        usoDeDisco = psutil.disk_usage('C:\\')
    elif(sistemaOperacional=="Linux"):
        usoDeDisco = psutil.disk_usage('/')

    usoDeCPU = psutil.cpu_percent(interval=1)
    freqDeCPU = psutil.cpu_freq()
    usoDeMemo = psutil.virtual_memory()

    qtdNucleos = psutil.cpu_count()
    qtdNucleosVirtuais = psutil.cpu_count(logical=False)

    nomeUsuario = psutil.users()[0].name
    qtdBateria = psutil.sensors_battery()[0]
    segundosParaAcabar = psutil.sensors_battery()[1]
    conectadoEnergia = psutil.sensors_battery()[2]


    i = i + 1

    # sql = "INSERT INTO registros (nomeMaquina, sistemaOperacional, qtdTotalMemoria, percentualMemoria, qtdTotalDisco, qtdUtilizadaDisco, percentualDisco, qtdNucleosCPU, qtdNucleosVirtuaisCPU, percentualCPU, frequenciaCPU) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # values = (nomeMaquina, sistemaOperacional, usoDeMemo.total, usoDeMemo.percent, usoDeDisco.total, usoDeDisco.used, usoDeDisco.percent, qtdNucleos, qtdNucleosVirtuais, usoDeCPU, freqDeCPU.current)
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

    Quantidade total de memória: {:d} GB
    Percentual de uso da memória: {:.2f}%

    Quantidade total de disco: {:d} GB
    Quantidade utilizada de disco: {:d} GB
    Percentual de uso do disco: {:.2f}%

    Nome da máquina: {:s}
    Sistema Operacional: {:s}
    Nome do usuário: {:s}

    Porcentagem de bateria disponível: {:d}
    Segundos até a bateria acabar: {:d}
    Está conectado na tomada? {:b}
    """.format(i, qtdNucleos, qtdNucleosVirtuais, usoDeCPU, freqDeCPU.current, 
               usoDeMemo.total, usoDeMemo.percent, 
               usoDeDisco.total, usoDeDisco.used, usoDeDisco.percent, 
               nomeMaquina, sistemaOperacional,
               nomeUsuario,
               qtdBateria, segundosParaAcabar, conectadoEnergia))
    time.sleep(5)

    controle = 0

    for process in psutil.process_iter():
        print("\n"+"PROCESSOS DO SISTEMA")
        print(f"ID: {process.pid}, Nome: {process.name()}, Status: {process.status()}")
        controle += 1
        if controle == 5:
            break

    print("##############################################################################################")





    
