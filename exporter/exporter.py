#!/usr/bin/python
import time
import os
import glob
import json
import flask
from flask import request
import RPi.GPIO as GPIO

#setup gpio
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#relay init open HIGH
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
relay = 0

#web
app = flask.Flask(__name__)

#init 1 wire sensor
base_dir = '/sys/bus/w1/devices/'

#raw temp
def read_temp_raw(sensor_id):
  device_folder = glob.glob(base_dir + '28*')[sensor_id]
  device_file = device_folder + '/w1_slave'
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

#clean temp
def read_temp(sensor_id):
  lines = read_temp_raw(sensor_id)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw(sensor_id)
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c

#metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
  current_temp1 = (read_temp(0))
  current_temp2 = (read_temp(1))
  return ('temperature_t1{temp="1",host="raspberrypi"} ' + str(current_temp1) + '\n' + 'temperature_t2{temp="2",host="raspberrypi"} ' + str(current_temp2) + '\n' + 'relay{host="raspberrypi"} ' + str(relay))

#relay control endpoint
@app.route('/relay', methods=['POST'])
def result():
  status = request.get_json(force=True)
  print(status)
  status = status['receiver']
  if status == 'cold-api':
    GPIO.output(12, GPIO.HIGH)
    global relay
    relay = 1
    return ('ok')
  else:
    GPIO.output(12, GPIO.LOW)
    global relay
    relay = 0
    return ('ok')

#go
app.run(host="0.0.0.0", port="5000")

