#
#
# Author: Aniruddha Gokhale
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, we use the "top" command and use it as producer of events for
#    Kafka. The consumer can be another Python program that reads and dumps the
#    information into a database OR just keeps displaying the incoming events on the
#    command line consumer (or consumers)
#

import os   # need this for popen
import time # for sleep
import sys
import requests
from kafka import KafkaProducer  # producer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

zip_code = sys.argv[1]
api_key = sys.argv[2]

URL = 'https://api.openweathermap.org/data/2.5/weather'
params = {'appid': api_key,
          'zip': f'{zip_code},us'}
		  
# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="129.114.25.80:9092", 
                                          acks=1)  # wait for leader to write to log
producer = KafkaProducer (bootstrap_servers="localhost:9092", 
                                          acks=1)

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range(100):
    
    # get the output of the top command
    #process = os.popen ("top -n 1 -b")
    # get the weather data
    response = requests.get(url=URL, params=params)
    # read the contents that we wish to send as topic content
    #contents = process.read()
	contents = response.json()

    # send the contents under topic utilizations. Note that it expects
    # the contents in bytes so we convert it to bytes.
    #
    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #
    #producer.send ("utilizations", value=bytes (contents, 'ascii'))
    #producer.flush ()   # try to empty the sending buffer

	producer.send(zip_code, value=bytes(str(contents), 'ascii'))
    producer.flush()   # try to empty the sending buffer
    # sleep a second
    time.sleep(2)

# we are done
producer.close()
    






