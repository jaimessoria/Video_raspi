###############################################################################
#
# Done by: Leandro Jaimes Soria
# Contact: https://www.linkedin.com/in/ljaimessoria/
#
# Program Description:
#
# Software in python that sends out emails to recipients from 
# a huge list (1 Mio entries) in a performant way.
#
# Execution
# python  PerformantEmailSender.py --dbfile db/db_file.csv 
###############################################################################

import asyncio
import signal
import argparse
import io
import logging
import sys
import os
import yaml
import logging.config
from queue import Queue
 
logger = logging.getLogger(__name__)
 
class EmailRoutines:
    def __init__(self):
        self.max_coroutines = 10           #number according to hardware resources
     
    async def email_sender (self, email_queue):
        while True:
            email = await email_queue.get()
            await asyncio.sleep(0.5)        # time to send an email
            email_state = 'Y'               # Y= email sent N = email NO sent
            logger.info(
                   "Sender: email: [%s] sent: [%s] ", email, email_state)

    def create_email_sender (self, email_queue):
        for x in range(self.max_coroutines):
            asyncio.ensure_future(self.email_sender(email_queue))

class DbRoutines:
 
   def email_counter (self, db_path: str):
       logger.info("Reading CSV ")  
       try:   
           num_email =100  # check in DB how many emails there is in the DB
           logger.info("The number of email to be send:[%i]", num_email)
       except Exception as e:
           logger.error('Reading from file failed')
           logger.error(str(e))
           sys.exit(1)
       return num_email
  
   async def email_fetcher (self, db_path: str, num_email: int, email_queue):
       while num_email > 0:
           await asyncio.sleep(0.2)    #time to fetch data from DB
           email = "email_"+str(num_email)+"@data.de"
           await email_queue.put(email)
           logger.info("Fetcher: num_email: [%i] email: [%s]", num_email, email)
           num_email -= 1
      
def parse_args():
   parser = argparse.ArgumentParser(
       description='Send emails in performant way')
 
   parser.add_argument('--dbfile', required=True,
                       help='Data Base file name')
 
   return parser.parse_args()
 
def setup_logging(
   default_path='logging.yaml',
   default_level=logging.INFO,
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
    email_routines = EmailRoutines()
    db_routines = DbRoutines()
    email_queue =  asyncio.Queue()
    loop = asyncio.get_event_loop()
 
    try:
        #args = parse_args()                                     # take de CSV file path
        email_routines.create_email_sender (email_queue)        # generate coroutines that will use the email queue
        num_email = db_routines.email_counter(args.dbfile)      # count de num of emails to send from DB               
        asyncio.ensure_future(db_routines.email_fetcher(
                               args.dbfile, num_email, email_queue))  #coroutine for reading emails from DB
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
       logger.info("Received exit signal")
       loop.close()
       sys.exit(1)

    logger.info('All operations completed successfully')
    sys.exit(0)
  
if __name__ == '__main__':
   main()