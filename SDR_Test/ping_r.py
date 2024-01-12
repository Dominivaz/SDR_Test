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

def ping_start(client):
    subprocess.check_output(["ping", "-c", "4", "-q", client], stderr=subprocess.DEVNULL)

def data_aqu():
    data = sdr.capture_data(nsamples=2048,nblocks=1)
    data = data
    print('Collected Data...')
    data1 = []
    while True:
        packet = conn.recv(4096)
        if not packet: break
            data1.append(packet)
    print('Received Data...')
    data1 = np.array(data1)
    data1 = pickle.loads(data1)
    print('Transcribed Data...')
    x = data*data1
    return x

def algorithm():
    mix = data_aqu()
    d_f = SDR_Test.receive_sync.receive_fitting(mix, mix.shape[1])
    changing = SDR_Test.receive_sync.receive_sync(d_f)
    dac.raw_value += int(changing)
    print('DAC Value Changed...')
    dac_values.append(dac.raw_value)

def save():
    if len(dac_values) <= 10:
        print('Will Save at 10:', len(dac_values))
        return
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    print(f'saved on {timestamp}')
    np.save(f'/home/pi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
    dac_values = []
    print('saved!')
    
####################################    

print('Script Started...')
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

dac.raw_value = 2010
sdr = ugradio.sdr.SDR(sample_rate = 3.2e6)
print('Initialized Everything...')
HOST = '10.32.92.219'
CLIENT = '10.32.92.210'
PORT = 2001
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((HOST, PORT))
receiver_socket.listen(1)
print('Waiting for Other Pi...')

conn, addr = receiver_socket.accept()

print('Communicating...')

dac_values = []

try:
    while True:
        ping_start(CLIENT)
        print('Pinged...')
        algorithm()
        print('Finished Algorithm...')
        save()
        print('Saved Last 10 Entries...')
except KeyboardInterrupt:
    print('Closing Connections and Saving Last Iteration...')
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    np.save(f'/home/pi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
    print('Saved Last Iteration...')
    conn.close()
    receiver_socket_close()
    print('Done!')
