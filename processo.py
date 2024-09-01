import psutil

for process in psutil.process_iter():
        print(f"ID: {process.pid}, Nome: {process.name()}, Status: {process.status()}")

        print(psutil.sensors_battery()[0])
        print(psutil.sensors_battery()[1])
        print(psutil.sensors_battery()[2])
        print(psutil.users()[0].name)