from time import sleep
import paho.mqtt.client as paho
import json
from threading import Thread
from queue import Queue

class TempSensor():
    id = 0
    temp = 0
    time = 0
    location = {
        'lat': 0,
        'lng': 0
    }
    def __init__(self, id, temp, time, location):
        self.id = id
        self.temp = temp
        self.time = time
        self.location = location
    def __iter__(self):
        return iter(self.id, self.temp, self.time, self.location) 
    def get(self):
        sensor = {'id':self.id,'temp':self.temp,'time':self.time,'location':self.location}
        return sensor
    def get_temp_time(self):
        return {
            'temp': self.temp,
            'time':self.time
        }

class TempSensorList():
    id = 0
    current_temp = 0
    current_time = 0
    prev_temp_time = []
    avg_temp = 0
    location = {
        'lat': 0,
        'lng': 0
    }
    def __init__(self, id, temp, time, location):
        self.id = id
        self.current_temp = temp
        self.current_time = time
        self.prev_temp_time = [{'temp':temp,'time':time}]
        self.avg_temp = temp
        self.location = location

    def __iter__(self):
        return iter(self.id, self.current_temp, self.current_time, self.prev_temp_time,self.avg_temp,self.location) 
    def get(self):
        sensor = {
            'id':self.id,
            'temp':self.current_temp,
            'time':self.current_time,
            'prev_temp_time':self.prev_temp_time,
            'avg_temp':self.avg_temp,
            'location':self.location
        }
        return sensor
    def add_temp(self, temp_time):
        if len(self.prev_temp_time) == 10:
            self.prev_temp_time.pop(0)
        self.prev_temp_time.append(temp_time)
        self.current_temp = temp_time['temp']
        self.current_time = temp_time['time']
        total = 0
        cnt = 0
        for i in self.prev_temp_time:
            total += i['temp']
            cnt += 1
        self.avg_temp = round(total/cnt, 2)

q = Queue()
temp_list = []
sorted_current = [] 
sorted_avg = []

def add_data( ):
    while True:
        b = True
        while not q.empty():
            #l1.acquire()
            global temp_list
            temp = q.get()
            if temp == None:
                continue
            for x in temp_list:
                if x.id == temp.id:
                    x.add_temp({'temp':temp.temp, 'time':temp.time})
                    b = False
                    break
            if b:
                temps = TempSensorList(temp.id, temp.temp, temp.time, temp.location)
                temp_list.append(temps)
            #l1.release()
            sleep(1)
        sleep(1)

def sort_current_temps():
    while True:
        global sorted_current
        sorted_current = sorted(temp_list, key=lambda x: x.current_temp, reverse=True)
        sleep(1)

def sort_avg_temps():
    while True:
        global sorted_avg 
        sorted_avg = sorted(temp_list, key=lambda x: x.avg_temp, reverse=True)
        sleep(1)

def publish_lists(client):
    while True:
        if not sorted_current and not sorted_avg:
            sleep(5)
            continue
        current_send = []
        avg_send = []
        for x in sorted_current:
            current_send.append(x.get())
        #     print(str(x.id) + " : " + str(x.current_temp))
        # print("=============================================")
        for y in sorted_avg:
            avg_send.append(y.get())
        #     print(str(y.id) + " : " + str(y.avg_temp))
        # print("=============================================")
        msg_current = str(json.dumps(current_send))
        msg_avg = str(json.dumps(avg_send))
        client.publish('/edge2/sorted_current', msg_current, qos=1)
        client.publish('/edge2/sorted_avg', msg_avg, qos=1)
        sleep(5)

def on_message(client, userdata, msg):
    msg = str(msg.payload).strip("'")
    msg = msg.strip("b'")
    res = json.loads(msg)
    temp = TempSensor(res['id'], res['temp'], res['time'],res['location'])
    q.put(temp)




def main():
    client = paho.Client()
    client.connect("broker.mqttdashboard.com", 1883)
    client.on_message = on_message
    client.subscribe("/219203655/edge2/+", qos=1)
    
    thread_add_data = Thread(target=add_data)
    thread_add_data.start()

    thread_sort_current = Thread(target=sort_current_temps)
    thread_sort_current.start()

    thread_sort_avg = Thread(target=sort_avg_temps)
    thread_sort_avg.start()

    thread_publish = Thread(target=publish_lists, args=[client])
    thread_publish.start()
    client.loop_forever()
    

if __name__=="__main__":
    main()