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
#    In this example, demonstrate Kafka streaming API to build a consumer.
#

import time
import sys
import json
import requests
from kafka import KafkaConsumer  # consumer of events

# Comma separated list of zip codes
zip_codes = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
db_ip = sys.argv[4]

# acquire the consumer
# (you will need to change this to your bootstrap server's IP addr)
consumer = KafkaConsumer(bootstrap_servers="localhost:9092")

# subscribe to topic
consumer.subscribe(topics=zip_codes.split(','))

# database address for storing data
db_address = f'http://{username}:{password}@{db_ip}:5984/couchdb'

# headers for sending data to database
headers = {
  'Content-Type': 'application/json'
}

# we keep reading and printing
for msg in consumer:
    # what we get is a record. From this record, we are interested in printing
    # the contents of the value field. We are sure that we get only the
    # utilizations topic because that is the only topic we subscribed to.
    # Otherwise we will need to demultiplex the incoming data according to the
    # topic coming in.
    #
    # convert the value field into string (ASCII)
    #
    # Note that I am not showing code to obtain the incoming data as JSON
    # nor am I showing any code to connect to a backend database sink to
    # dump the incoming data. You will have to do that for the assignment.
    json_data = msg.value.decode('utf-8').replace("\'", "\"")
    response = requests.request("POST", db_address, headers=headers, data=json_data)

    print(json_data)
    print(response.json())

    # CouchDB gets overloaded when results come too fast
    # So pause between requests
    time.sleep(10)

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close()
    






