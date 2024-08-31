import psutil

for process in psutil.process_iter():
        print(f"ID: {process.pid}, Nome: {process.name()}, Status: {process.status()}")