import os
import time
#from gpiozero import CPUTemperature
#from time import sleep, strftime, time

NAS = '192.168.0.135:/Users/Leo/Documents/Raspi'
folder = '/mnt/nfs'
t_cap = 10
cpu = CPUTemperature(min_temp=50, max_temp=90)

print("Start record")
for i in range(2):
    #Mount NAS 
    command = 'sudo mount -t nfs '+ NAS +' '+folder
    os.system(command)    
    #Capture Video
    file_name= folder + time.strftime("/1080p30_b12-%Y%m%d-%H%M%S")
    command = 'raspivid -t'+ str(tcap*100) +'-w 1436 -h 1080 -fps 30 -b 12000000 -o '+file_name +'.h264'
    os.system(command)
    sleep(t_cap)
    #convert video to mp4
    command= 'MP4Box -fps 30 -add '+file_name+ '.h264 '+ file_name +'.mp4'
    os.system(command)
    # log temperature
    log = open(folder+"cpu_temp.csv", "a")
    log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),cpu.temperature))
    log.close()
    #sleep(1)
#unmount NAS
command = 'sudo umount /mnt/nfs'
os.system(command)   
print("finish record")