import paho.mqtt.client as mqtt
import serial
from time import sleep



MQTT_ADDRESS = "192.168.*.*" #Her må resten av IP-addressen skrives inn
MQTT_USER = "********"
MQTT_PASSWORD = "*************"
MQTT_TOPIC_POTMETER = "potmeter"
MQTT_TOPIC_ULTRASOUND = "ultrasound"
MQTT_TOPIC_DOPPLERRADAR= "doppler-radar"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_POTMETER)
    client.subscribe(MQTT_TOPIC_ULTRASOUND)
    client.subscribe(MQTT_TOPIC_DOPPLERRADAR)

def on_message(client, userdata, msg):
    print(msg.topic + '  '+ str(msg.payload))

 

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    
    mqtt_client.loop_forever()
    ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
    while True:
        mqtt_client.loop_start()
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)                   #print received data
        mqtt_client.loop_stop()                 
    # ser.write(received_data)                #transmit data serially 
 

if __name__ == '__main__':
    print("MQTT to InfluxDB bridge")
    main()



