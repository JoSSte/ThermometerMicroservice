import glob
import time
import json
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime
import platform


app = Flask(__name__)
api = Api(app)
os = platform.system()
file_name = '/w1_slave'

if os == 'Linux':
    base_dir = '/sys/bus/w1/devices/'
    delimiter = '/'
elif os == 'Windows':
    # testing on windows
    base_dir = 'test/'
    delimiter = '\\'

DEVICE_LIST = {
    #'28-dummy-01': {'last_reading': 0, 'name': 'someName'}
}

actual_devices = [ f.split(delimiter)[-1] for f in glob.glob(base_dir + '28*')]

class TempSensor:
    def serialize(self):
        return  {
            'sensor_id': self.id
        }

    def setName(self, name):
        self.name 

    def __init__(self, id, name = ''):
        self.id = id
        self.name = name

class TempReading:
    def serialize(self):
        return  {
            'temperature': self.temp,
            'sensor': {
                'name': self.sensor.name,
                'id': self.sensor.id,
                'trend': self.trend
            },
            'date': self.date
        }
    def setTrend(self, trend):
        self.trend = trend

    def __init__(self, t, s):
        self.temp = t
        self.sensor = s
        self.date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        self.trend = 'unknown'

def read_temp_raw(device_id):
    f = open(base_dir +  device_id + file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_id):
    lines = read_temp_raw(device_id)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(round(float(temp_string) / 1000.0))
        return temp_c

#parser = reqparse.RequestParser()
#parser.add_argument('task')

def abort_if_sensor_doesnt_exist(sensor_id):
    if sensor_id not in actual_devices:
        abort(404, message="Device ID {} doesn't exist".format(sensor_id))

class Temperature(Resource):
    def get(self, sensor_id):
        abort_if_sensor_doesnt_exist(sensor_id)
        s = TempSensor( sensor_id)
        r = TempReading(read_temp(sensor_id), s)
        return r.serialize()

class TemperatureList(Resource):
    def get(self):
        sensors = []
        for sensor_id in actual_devices:
            s = TempSensor(sensor_id)
            r = TempReading(read_temp(sensor_id), s)
            sensors.append(r)
            if sensor_id in DEVICE_LIST:
                if DEVICE_LIST[sensor_id]['last_reading'] < r.temp:
                    r.setTrend('rising')
                elif DEVICE_LIST[sensor_id]['last_reading'] > r.temp:
                    r.setTrend('falling')
                elif DEVICE_LIST[sensor_id]['last_reading'] == r.temp:
                    r.setTrend('steady')
                else:
                    r.setTrend('unknown')
                DEVICE_LIST[sensor_id]['last_reading'] = r.temp
            else:
                DEVICE_LIST[sensor_id] = {'last_reading' : r.temp}
                #DEVICE_LIST[sensor_id]['last_reading'] = r.temp
        return jsonify(sensorlist=[s.serialize() for s in sensors])

##
## Actually setup the Api resource routing here
##
api.add_resource(TemperatureList, '/temp')
api.add_resource(Temperature, '/temp/<sensor_id>')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=80)
