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
if os == 'Linux':
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
elif os == 'Windows':
    # testing on windows
    device_file = 'w1_slave.txt'

class TempSensor:
    def get_objects(self):
        data = {
            'sensor_id': self.id
        }
        return jsonify(data)

    def __init__(self, n, i, f):
        self.id = i
        self.name = n
        self.file = f

class TempReading:
    def get_objects(self):
        data = {
            'temperature': self.temp,
            'sensor': {
                'name': self.sensor.name,
                'id': self.sensor.id
            },
            'date': self.date
        }
        return jsonify(data)

    def __init__(self, t, s):
        self.temp = t
        self.sensor = s
        self.date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Temperature(Resource):
    def get(self):
        s = TempSensor('vand_ud', '28-dummy', device_file)
        r = TempReading(read_temp(), s)
        return r.get_objects()

##
## Actually setup the Api resource routing here
##
api.add_resource(Temperature, '/temp')
#api.add_resource(Temperature, '/temp/<sensor_id>')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')