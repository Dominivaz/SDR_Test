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

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725(i2c)

dac.raw_value = 2010
sdr = ugradio.sdr.SDR(sample_rate = 3.2e6)
HOST = '10.32.92.219'
PORT = 2001
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((HOST, PORT))
receiver_socket.listen(1)#move into loop?

addr = 0

conn, addr = receiver_socket.accept()#move into loop?

start = 2
syncing = 2

dac_values = []
save = 1
try:
    while syncing == 2:
        print('havent received start...')
        if addr != 0:
            start += 1
            syncing -= 1
            print('starting...')
    
    while start == 3:
        
#            save = 1
        print('capturing data')
        data = sdr.capture_data(nsamples = 2048, nblocks = 1)
#         data = np.mean(data, axis = 0)
        data = data[0]
        print('data captured')
        data1 = conn.recv(4096)#change, or use exact for the amount in an array; 64 bytes per 1 block sample
        data1 = data1.decode()
        print('received data')
        data1 = eval(data1)
        print('converted received data')
        
        x = data*data1
        print('mixed')
        d_f = SDR_Test.receive_fitting(x)
        changing = SDR_Test.receive_sync(d_f)
        dac.raw_value += changing
        
        print(f'DAC value changed by {changing}')
        print(f'New DAC value should be: {dac.raw_value}')
#            dac.raw_value #unnecessary?
        dac_values.append(dac.raw_value)

        save += 1        
        if save == 10:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            print(f'saved on {timestamp}')
            np.save(f'home/pi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
            print('saved!')
            save -= 9
        
except KeyboardInterrupt:
    print('Closing connections and saving last interation.')
    
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    np.save(f'home/pi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
    
    conn.close()
    receiver_socket_close()
    print('Done!')