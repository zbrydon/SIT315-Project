const express = require('express');
const app = express();
const mqtt = require('mqtt');
const client = mqtt.connect("mqtt://broker.hivemq.com:1883");
const port = process.env.PORT || 3000;
const base = `${__dirname}/public`;

app.use(express.static('public'));

app.use(function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
});

client.on('connect', () => {
    console.log('mqtt connected');
});

let current_sensors = [];
let avg_sensors = [];


client.subscribe('/edge1/sorted_current');
client.subscribe('/edge1/sorted_avg');
client.subscribe('/edge2/sorted_current');
client.subscribe('/edge2/sorted_avg');

prev_msg =''

client.on('message', (topic, message) => {
    let x = topic.split("/");
    switch(x[2]) {
        case "sorted_current":
            msg = JSON.parse(message);
            msg.forEach(sensor => {
                let obj = current_sensors.find(x => x.id === sensor.id)
                if(obj){
                    let index = current_sensors.indexOf(obj);
                    current_sensors[index] = sensor;
                }else{
                    current_sensors.push(sensor)
                }
            });
            
            break;
        case "sorted_avg":
            msg = JSON.parse(message);
            msg.forEach(sensor => {
                let obj = avg_sensors.find(x => x.id === sensor.id)
                if(obj){
                    let index = avg_sensors.indexOf(obj);
                    avg_sensors[index] = sensor;
                }else{
                    avg_sensors.push(sensor)
                }
            });
            
            break;
        default:
            break;   
    }
})

app.get('/current', (req, res) => {
    current_sensors.sort((a, b) => {
        return b.temp - a.temp;
    });
    return res.send(current_sensors);
})

app.get('/avg', (req, res) => {
    avg_sensors.sort((a, b) => {
        return b.avg_temp - a.avg_temp;
    });
    return res.send(avg_sensors);
})


app.listen(port, () => {
    console.log(`listening on port ${port}`);
});

app.get('/', function (req, res) {
    res.sendFile(`${base}/home.html`);
});


app.get('*', (req, res) => {
    res.sendFile(`${base}/404.html`);
}); 