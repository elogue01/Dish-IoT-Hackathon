import RPi.GPIO as GPIO
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def message_to_awsiot(topic, payload):
"""
This helper function delivers a message from the a registered raspberry pi IoT
device to AWSIoT.
INPUT: topic - string
       payload - json
OUTPUT: a json message is delivered to AWSIoT which is then parsed and delivered
        to a DynamoDB
"""
    # For certificate based connection
    myMQTTClient = AWSIoTMQTTClient("SeatIT-pi-sensor")

    # Configurations
    # Note: This instance is no longer active
    myMQTTClient.configureEndpoint("a1hfvkkil1prq6.iot.us-west-2.amazonaws.com", 8883)
    # Note: These AWSIot credentials are no longer any good
    myMQTTClient.configureCredentials("/home/pi/deviceSDK/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem", "/home/pi/deviceSDK/140d68dffd-private.pem.key", "/home/pi/deviceSDK/140d68dffd-certificate.pem.crt")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec

    myMQTTClient.connect()
    myMQTTClient.publish(topic, payload, 1)
    myMQTTClient.disconnect()

"""
The following code runs on the raspberry with PIR (proximity) sensor in order to
update seat occupancy status and deliver a change in occupancy state to AWSIoT
which then feeds this information into an AWS DynamoDB (noSQL database)
"""

sensor = 17 # pin id on the pi

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

# initialize the seat occupancy states
previous_state = False
current_state = False

# topics allow you to catagorize and search for messages in AWSIoT
topic = 'seatit/occupied'

# The SeatIt detector code is run as a continuos while loop
while True:
    time.sleep(1)
    # First check if the seat is occupied
    if current_state == True:
        state = []
        # The sensor monitors an occupied seat for movement
        # The range can be adjusted to monitor over a longer/shorter time interval
        # We don't want to revert the seat to unoccupied unless there has been
        # no sensor activity over a defined time interval
        for _ in range(10):
            time.sleep(1) # adds some pause to the loop
            state.append(GPIO.input(sensor))
            # Movement at anytime over this time interval will restart the loop
            if True in state:
                current_state = True
                print(state)
                break
        # A final check to determine if there was movement over the time interval
        if True in state:
                current_state = True
                print(state)
        # The lack of sensor activity reverts the seat to an unoccupied state
        else:
            current_state = False
            new_state = "Occupied" if current_state else "Unoccupied"
            print("GPIO pin %s is %s" % (sensor, new_state))
            print(state)
            # deliver a json meassage to AWSIoT about the change in occupancy
            payload = json.dumps(dict(SeatNumber = int(1), SeatName= str('bob'), Occupied=current_state))
            message_to_awsiot(topic, payload)

    # when the seat is unoccupied monitor for sensor activity
    else:
        previous_state = current_state
        current_state = GPIO.input(sensor) # delivered as a 1 or 0
        # Detect a change in occupancy
        if current_state != previous_state:
            new_state = "Occupied" if current_state else "Unoccupied" # change state
            print("GPIO pin %s is %s" % (sensor, new_state))
            current_state = bool(current_state) # change 1 or 0 to boolean
            # deliver a json meassage to AWSIoT about the change in occupancy
            payload = json.dumps(dict(SeatNumber = int(1), SeatName= str('bob'), Occupied=current_state))
            message_to_awsiot(topic, payload)
