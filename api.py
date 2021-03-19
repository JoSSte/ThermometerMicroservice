import glob
import time
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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
        return read_temp(), datetime.now()

##
## Actually setup the Api resource routing here
##
api.add_resource(Temperature, '/temp')
#api.add_resource(Temperature, '/temp/<sensor_id>')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')