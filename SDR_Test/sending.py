import numpy as np
import socket
import pickle
import ugradio
import datetime
import time

sdr = ugradio.sdr.SDR(sample_rate = 3.2e6)

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'ip on ethernet pi'
PORT = 2001
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.connect((HOST, PORT))

start_data = b'start'

sender_socket.sendall(start_data)
times = []
save = 1
try:
    while True:
        data = sdr.capture_data(nsamples = 2048, nblocks = 10)
        data = np.mean(data, axis = 0)
        
        data = pickle.dumps(data)
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        times.append(timestamp)
        print(f'sending data on {timestamp}...')
        sender_socket.sendall(data)
        print('data sent!')
        save += 1
        if save = 10:
            print('saving time when data was sent...')
            np.save(f'home/pi/rec_times/time_{timestamp}', np.array(times, dtype='object'))
            print('time was saved')
            save -= 9
#         time.sleep(1)
except KeyboardInterrupt:
    print('Saving and closing.')
    np.save(f'home/pi/rec_times/time_{timestamp}', np.array(times, dtype='object'))
    sender_socket.close()
    print('Done!')