import numpy as np
import matplotlib.pyplot as plt
import ugradio
import SDR_Test
import datetime
import time
import board
import busio
import adafruit_mcp4725
from SDR_Test import receive_sync_test30
import os

print('Started Script...')

#f_sample_prime = 28.8e6

#sdr = ugradio.sdr.SDR(sample_rate = 3.2e6, direct=True)
sdr = ugradio.sdr.SDR(direct=True)

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

#dac.raw_value = 2014
dac.raw_value = 0
#dac.raw_value = 4095

nsamples = 8192
loops = 20

file_number = '37/'
os.mkdir('/home/radiopi/sync_data/new_SI/dac' + file_number)
os.mkdir('/home/radiopi/sync_data/new_SI/wave' + file_number)
os.mkdir('/home/radiopi/sync_data/new_SI/d_f' + file_number)

print('Everything Initialized...')

dac_values = []
saved_data = []
d_f_values = []

start = 0
stop = nsamples

save = 0

#sdr.capture_data()

#sdr.capture_data()

#print('Cleaned SDR...')

try:
    
    while True:
        collected = []
        #data = []
        #for i in range(30):
         #   collect = sdr.capture_data(nblocks=1)[0]
          #  data.append(collect)
        #data = np.array(data)
        #data = sdr.capture_data(nsamples=4096, nblocks=1)[0,::2]
        data = sdr.capture_data(nsamples=nsamples, nblocks=loops)
        for i in np.arange(1, loops):
            df = SDR_Test.receive_sync_test30.receive_fitting(data[i], data[i].shape, start, stop, f_sample=sdr.get_sample_rate(), tone=.2e6)
            collected.append(df)
            start += nsamples
            stop += nsamples
        #data = np.mean(data, axis =0)
        
        beginning = time.time()
        
        print('Captured Data...')
        #print('shape of data:', data.shape)
        #d_f = receive_sync.receive_fitting(data, data.shape, f_sample=3.2e6, tone=.2e6)
        #d_f = receive_sync_test30.receive_fitting(data, data.shape, start, stop, f_sample=sdr.get_sample_rate(), tone=.2e6)
        df_ave = np.array(collected)
        average = np.mean((df_ave))
        std = np.std((df_ave))
        thresh = 1
        filtered = (df_ave)[abs((df_ave)-average) <= thresh * std]
        average = np.mean(filtered)
        print('frequency diff:', average)
        changing = receive_sync_test30.receive_sync(average)
        print('changing:', int(changing))
        dac.raw_value += int(changing)
        print('f_sample_prime:', dac.raw_value)
        saved_data.append(data)
        dac_values.append(dac.raw_value)
        d_f_values.append(average)
        print(np.array(d_f_values).shape)
        save += 1
        
        ending = time.time()
        delay = np.round((ending - beginning)*sdr.get_sample_rate())
        #start += int(delay)
        #stop += int(delay)
        
        print('Took this long:', delay)
        
        if save == 100:
            
            save_start = time.time()
            
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            print(f'saved on {timestamp}')
            np.save('/home/radiopi/sync_data/new_SI/dac' + file_number + f'/dac_values_{timestamp}', np.array(dac_values))
            np.save('/home/radiopi/sync_data/new_SI/wave' + file_number + f'/recorded_data_{timestamp}', np.array(saved_data))
            np.save('/home/radiopi/sync_data/new_SI/d_f' + file_number + f'/d_f_{timestamp}', np.array(d_f_values))
            print('saved!')
            dac_values = []
            saved_data = []
            d_f_values = []
            save = 0
            
            save_ending = time.time()
            save_delay = np.round((save_ending - save_start)*sdr.get_sample_rate())
            #start += int(save_delay)
            #stop += int(save_delay)
            
except KeyboardInterrupt:
    print('Closing...')
#    current_time = datetime.datetime.now()
#    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
#    np.save(f'/home/radiopi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
#    print('Saved Last Iteration...')
#    plt.figure()
#    plt.plot(data)
#    plt.show()
    print('Done!')
