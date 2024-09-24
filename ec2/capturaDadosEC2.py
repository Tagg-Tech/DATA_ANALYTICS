import psutil
import time
import platform
from socket import gethostname
import pandas as pd


nomeMaquina = gethostname()  
sistemaOperacional = platform.system()

    


def capturarDf():
    column_names = ['idDados', 'dataHora', 'percCPU', 'tempoInativo', 'percRAM', 'percDisc', 'usedDisc', 'fkNotebook']

    df = pd.DataFrame(columns=column_names)
    i = 0

    while i < 5:

    # Criar o DataFrame vazio com as colunas definidas

        if(sistemaOperacional=="Windows"):
            usoDeDisco = psutil.disk_usage('C:\\')
        elif(sistemaOperacional=="Linux"):
            usoDeDisco = psutil.disk_usage('/')

        usoDeCPU = psutil.cpu_percent(interval=1)
        freqDeCPU = psutil.cpu_freq()
        usoDeMemo = psutil.virtual_memory()


        i = i + 1

        values = (usoDeMemo.percent, usoDeDisco.used, usoDeDisco.percent, usoDeCPU, freqDeCPU.current)
        data = pd.Timestamp.now()
        data_formatada = data.strftime('%Y-%m-%d_%H-%M-%S')
        dados = {
        'idDados': i,
        'dataHora': data,
        'percCPU': freqDeCPU.current ,
        'tempoInativo': freqDeCPU.current,
        'percRAM': usoDeMemo.percent,
        'percDisc': usoDeDisco.percent,
        'usedDisc': usoDeDisco.used,
        'fkNotebook': 101
    }
        novo_df = pd.DataFrame([dados])

    # Concatenar os dados ao DataFrame original
        df = pd.concat([df, novo_df], ignore_index=True)

        print(df)

    
        print(freqDeCPU)

        time.sleep(1)

        
        print("##############################################################################################")
        
    df.to_csv(f'{data_formatada}.csv', index=False)
    
    
while True:
    capturarDf()