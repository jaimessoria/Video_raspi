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
import signal
import argparse
import io
import logging
import yaml
import logging.config
from queue import Queue
import os
import time
from gpiozero import CPUTemperature
from time import sleep, strftime, time
 
NAS = '192.168.0.135:/Users/Leo/Documents/Raspi'
folder = '/mnt/nfs'
cpu = CPUTemperature(min_temp=50, max_temp=90)
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
    async def record_video (self,folder,duration_s):
        while True:
            try:   
                #Capture Video
                file_name= folder + strftime("/1080p30_b12-%Y%m%d-%H%M%S")
                command = 'raspivid -t '+ str(duration_s*100) +' -w 1436 -h 1080 -fps 30 -b 12000000 -o '+file_name +'.h264' 
                os.system(command)
                logger.info("Recording: %s",file_name)
                await asyncio.sleep(duration_s)
            except Exception as e:
                logger.error('Recording failed')
                logger.error(str(e))

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
    #email_queue =  asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        #Mount NAS 
        command = 'sudo mount -t nfs '+ NAS +' '+folder
        os.system(command) 
        logger.debug('NAS mounted')
        #Threads
        asyncio.ensure_future(temp_routine.temp_logger(10))    #coroutine for temp log
        asyncio.ensure_future(video_routine.record_video(folder,50))  #coroutine for video recording

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