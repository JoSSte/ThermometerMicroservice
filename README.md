# ThermometerMicroservice
Python based Microservice to run on an old pi with 1-wire thermometer DS18b20

## Description
Basically a python rest service to read multiple 1-wire attached DS18b20 sensors and display the results as a microservice for Home automation.

## References
* Reading the sensor
    * [Adafruit's Raspberry Pi_DS18B20 Temperature Sensing Lesson](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/master/Raspberry_Pi_DS18B20_Temperature_Sensing/thermometer.py)
    * https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
* Serving the REST API
    * https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
    * https://flask-restful.readthedocs.io/en/latest/