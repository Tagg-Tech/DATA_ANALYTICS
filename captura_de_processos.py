import psutil
import mysql.connector

db_connection = mysql.connector.connect(host='localhost', user='root', password='150621', database='teste')
cursor = db_connection.cursor()


for process in psutil.process_iter():
        print("\n"+"PROCESSOS DO SISTEMA")
        print(f"ID: {process.pid}, Nome: {process.name()}, Status: {process.status()}")
        
        processo = process.name()

        sql2 = "insert into processos (nome) VALUES (%s)"
        values2 = (processo,)
        cursor.execute(sql2, values2)
        db_connection.commit()
