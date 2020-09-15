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
    async def temp_logger (self,folder,period):
        while True:
            try:   
                # log temperature
                logger.info("temp: %i",cpu.temperature)
                await asyncio.sleep(period)
            except Exception as e:
                logger.error('Reading temperature failed')
                logger.error(str(e))

async def shutdown(loop):

    logging.info("Closing threads")
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

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
    #email_queue =  asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        #Mount NAS 
        command = 'sudo mount -t nfs '+ NAS +' '+folder
        os.system(command) 
        logger.debug('NAS mounted')
        #Threats 
        asyncio.ensure_future(temp_routine.temp_logger(folder,10)) #coroutine for temp log
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logger.debug("Received exit signal")

        command = 'sudo umount /mnt/nfs'
        os.system(command) 
        logger.debug('NAS umounted')

        for task in asyncio.Task.all_tasks():
            task.cancel()
        loop.stop()
        logger.debug('closing thread')
  
if __name__ == '__main__':
   main()