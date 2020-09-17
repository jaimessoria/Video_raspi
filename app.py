###############################################################################
#
# Done by: Leandro Jaimes Soria
# Contact: https://www.linkedin.com/in/ljaimessoria/
#
# Program Description:
#
# Software in python that capture video, store in NAS and compress to MP4
# The hardware used was: Rasberry pi 4 + Camera Module v1
#
# Execution
# python  app.py 
###############################################################################

import asyncio
import logging
import yaml
import logging.config
import os
import time
from queue import Queue
from gpiozero import CPUTemperature
from time import sleep, strftime, time
import subprocess,shlex
#from pythonping import ping
 
NAS = '192.168.0.135:/Users/Leo/Documents/Raspi'
folder = '/mnt/nfs'
cpu = CPUTemperature(min_temp=30, max_temp=90)
logger = logging.getLogger(__name__)

class TempRoutines:    
    async def temp_logger (self,period_s):
        while True:
            try:   
                # log temperature
                logger.info("temp: %i",cpu.temperature)
                await asyncio.sleep(period_s)
            except Exception as e:
                logger.error('Reading temperature failed')
                logger.error(str(e))

class VideoRoutines:
    def __init__(self,symbol=None):
        self.Stp_time_s = 2

    async def record_video_m (self,folder,duration_m,video_queue):
        while True:
            try:   
                #Capture Video
                file_name= folder + strftime("/1080p25-%Y%m%d-%H%M%S")
                logger.info("Recording: %s",file_name)
                command= shlex.split('raspivid -t '+ str(duration_m*60000) + 
                    ' -w 1436 -h 1080 -a 12 -drc high -fps 25 -b 17000000 -o '
                    + file_name +'.h264')
                p3 = subprocess.Popen(command)
                await asyncio.sleep(duration_m*60+self.Stp_time_s)
                await video_queue.put(file_name)
            except Exception as e:
                logger.error('Recording failed')
                logger.error(str(e))
                p3.terminate()

    async def wrap_video (self,video_queue):
        del_h264 = False
        prev_file_name = ''
        while True:
            try:   
                #convert video to mp4
                file_name = await video_queue.get()
                if del_h264:
                    del_h264 = False
                    logger.debug("Delete: %s.h264",prev_file_name)
                    command= shlex.split('sudo rm '+ prev_file_name +'.h264 ')
                    p2 = subprocess.Popen(command)

                logger.debug("Wrap to MP4: %s",file_name)
                command= shlex.split('MP4Box -fps 25 -add ' 
                        +file_name+ '.h264 '+ file_name +'.mp4')
                p = subprocess.Popen(command)
                del_h264 = True
                prev_file_name = file_name
            except Exception as e:
                logger.error('warping failed')
                logger.error(str(e))
                p.terminate()
                p2.terminate()

def setup_logging(
   default_path='logging.yaml',
   default_level=logging.DEBUG,
   env_key='LOG_CFG'
):
   """Setup logging configuration"""
   path = default_path
   value = os.getenv(env_key, None)
   if value:
       path = value
   if os.path.exists(path):
       with open(path, 'rt') as f:
           config = yaml.safe_load(f.read())
       logging.config.dictConfig(config)
   else:
       logging.basicConfig(level=default_level)
 
def main():
    setup_logging()
    logger.info('Running. Press CTRL-C to exit.')
    temp_routine = TempRoutines()
    video_routine = VideoRoutines()
    video_queue =  asyncio.Queue()
    loop = asyncio.get_event_loop()

#    response = ping('192.168.0.135', size=40, count=10)
#    while not response.success:
    logger.info('waiting NAS')
    sleep(60)
#        response = ping('192.168.0.135', size=40, count=10)
#        #r = pyping.ping(NAS)

    try:
        #Mount NAS 
        command = 'sudo mount -t nfs '+ NAS +' '+folder
        os.system(command) 
        logger.debug('NAS mounted')
        #Threads
        asyncio.ensure_future(
            video_routine.record_video_m(folder,1,video_queue))  #coroutine for video recording
        asyncio.ensure_future(
            temp_routine.temp_logger(1))    #coroutine for temp log
        asyncio.ensure_future(
            video_routine.wrap_video(video_queue))  #coroutine for video recording
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logger.debug("Received exit signal")

        command = 'sudo umount /mnt/nfs'
        os.system(command) 
        logger.debug('NAS umounted')

        logger.debug('closing thread')
        for task in asyncio.Task.all_tasks():
            task.cancel()
        loop.stop()
  
if __name__ == '__main__':
   main()