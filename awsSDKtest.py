# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

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
payload = json.dumps(dict(SeatNumber = int(1), SeatName= str('bob'), Occupied=True))
myMQTTClient.publish('seatit/occupied', payload, 1)
myMQTTClient.disconnect()
