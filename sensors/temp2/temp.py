from time import sleep
import paho.mqtt.client as paho
import json
import random
import datetime

edge = 'edge1'

class TempSensor():
    id = 2
    temp = 0
    time = 0
    location = {
        'lat': 0,
        'lng': 0
    }
    def __iter__(self):
        return iter(self.id, self.temp, self.time, self.location) 
    def get(self):
        sensor = {
            'id':self.id,
            'temp':self.temp,
            'time':self.time,
            'location':self.location
        }
        return sensor

def generate(temp_sensor, client):
    temp_sensor.location = {
        'lat': round(random.uniform(-85, 85), 4),
        'lng': round(random.uniform(-180, 180), 4),
    }
    while(True):
        temp_sensor.temp = round(random.uniform(10,40), 2)
        temp_sensor.time = str(datetime.datetime.now())

        msg = str(json.dumps(temp_sensor.get()))
        client.publish('/219203655/{edge}/temp{id}'.format(edge=edge, id=temp_sensor.id), msg, qos=1)
        print(msg)
        sleep(5)



def main():
    client = paho.Client()
    client.connect("broker.mqttdashboard.com", 1883)
    temp_sensor = TempSensor()

    generate(temp_sensor, client)
    

if __name__=="__main__":
    main()
