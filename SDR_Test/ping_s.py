import numpy as np
import socket
import pickle
import ugradio
import SDR_Test
import datetime
import time
import board
import busio
import adafruit_mcp4725
import subprocess

def ping(host):
    try:
        subprocess.check_output(["ping", "-c", "1", "-q", host], stderr=subprocess.DEVNULL)
        print('Ping Received...')
        return True
    except subprocess.CalledProcessError:
        return False

def ping_func():
    data = sdr.capture_data(nsamples=2048,nblocks=1)
    data = data[0]
    data = pickle.dumps(data)
    sender_socket.sendall(data)
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    times.append(timestamp)
    print('Data Sent...')
    
def save():
    if len(times) <= 10:
        print('Will Save at 10:', len(times))
        return
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    np.save(f'home/pi/rec_times/time_{timestamp}', np.array(times, dtype='object'))
    times = []
    print('saved!')
    
#####################    
    
sdr = ugradio.sdr.SDR(sample_rate = 3.2e6)
print('SDR Initialized...')

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '10.32.92.219'
PORT = 2001
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.connect((HOST, PORT))
print('Communicating...')

times = []

print('starting')

try:
    while True:
        print('Waiting on Ping...')
        result = ping(HOST)
        save()
        if result:
            ping_func()
except KeyboardInterrupt:
    print('Saving and closing.')
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    np.save(f'home/pi/rec_times/time_{timestamp}', np.array(times, dtype='object'))
    sender_socket.close()
    print('Done!')