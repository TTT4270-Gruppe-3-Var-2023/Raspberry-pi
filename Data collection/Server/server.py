'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
#Her er RPI-Sub.py forsøkt implementert. Har ikke fått kodene til å funke sammen som en kode enda. Tror ett problem er to evige løkker.
#sjekk hva .loop_forever() er brukt.
import serial
from time import sleep
import paho.mqtt.client as mqtt
from multiprocessing import Process

MQTT_ADDRESS = "192.168.43.206" #Her må resten av IP-addressen skrives inn
MQTT_USER = "Gruppe3"
MQTT_PASSWORD = "(XWtp·/3gzPylsW"
MQTT_TOPIC_POTMETER = "potmeter"
MQTT_TOPIC_ULTRASOUND = "ultrasound"
MQTT_TOPIC_DOPPLERRADAR = "doppler-radar"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_POTMETER)
    client.subscribe(MQTT_TOPIC_ULTRASOUND)
    client.subscribe(MQTT_TOPIC_DOPPLERRADAR)

def on_message(client, userdata, msg):
    print(msg.topic + '  '+ str(msg.payload))

 


    

def loop_a():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

def loop_b():
    ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        received_data = str(received_data)
        print (float(received_data.replace("b'","").replace("'","")))                   #print received data
        

if __name__ == '__main__':

    print("Data\n")
    Process(target=loop_a).start()
    Process(target=loop_b).start()






