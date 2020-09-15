from gpiozero import CPUTemperature
from time import sleep, strftime, time


cpu = CPUTemperature(min_temp=50, max_temp=90)

print("Start record")
for i in range(100):
    log = open("cpu_temp.csv", "a")
    log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),cpu.temperature))
    log.close()
    sleep(1)
print("finish record")