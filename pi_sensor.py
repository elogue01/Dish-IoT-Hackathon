import RPi.GPIO as GPIO
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

sensor = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False
topic = 'seatit/occupied'

def message_to_awsiot(topic, payload):
    # For certificate based connection
    myMQTTClient = AWSIoTMQTTClient("SeatIT-pi-sensor")
    # For Websocket connection
    # myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
    # Configurations
    # For TLS mutual authentication
    myMQTTClient.configureEndpoint("a1hfvkkil1prq6.iot.us-west-2.amazonaws.com", 8883)
    # For Websocket
    # myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
    myMQTTClient.configureCredentials("/home/pi/deviceSDK/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem", "/home/pi/deviceSDK/140d68dffd-private.pem.key", "/home/pi/deviceSDK/140d68dffd-certificate.pem.crt")
    # For Websocket, we only need to configure the root CA
    # myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    #myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    myMQTTClient.connect()
    myMQTTClient.publish(topic, payload, 1)
    myMQTTClient.disconnect()

while True:
    time.sleep(1)
    if current_state == True:
        state = []
        for _ in range(10):
            time.sleep(1)
            state.append(GPIO.input(sensor))
            if True in state:
                current_state = True
                print(state)
                break
        if True in state:
                current_state = True
                print(state)
        else:
            current_state = False
            new_state = "Occupied" if current_state else "Unoccupied"
            print("GPIO pin %s is %s" % (sensor, new_state))
            print(state)
            payload = json.dumps(dict(SeatNumber = int(1), SeatName= str('bob'), Occupied=current_state))
            message_to_awsiot(topic, payload)
        
    else:
        previous_state = current_state
        current_state = GPIO.input(sensor)
        if current_state != previous_state:
            new_state = "Occupied" if current_state else "Unoccupied"
            print("GPIO pin %s is %s" % (sensor, new_state))
            current_state = bool(current_state)
            payload = json.dumps(dict(SeatNumber = int(1), SeatName= str('bob'), Occupied=current_state))
            message_to_awsiot(topic, payload)
        
