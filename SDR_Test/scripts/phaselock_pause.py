import numpy as np
import ugradio
import SDR_Test
import datetime
import time
import board
import busio
import adafruit_mcp4725
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def files(file_number):
    os.mkdir('/home/radiopi/sync_data/sdr/pause/dac_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/pause/d_f_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/pause/wave_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/pause/unix_values' + file_number)

    
parser = ArgumentParser(description = 'files', formatter_class = ArgumentDefaultsHelpFormatter)

parser.add_argument('-f', dest = 'file_number_', type = int, help = 'File number for data')
parser.add_argument('-n', dest = 'fs_number_', type = float, default = 2.2, help = 'Sampling frequency for SDR in MHz')
parser.add_argument('-s', dest = 'sample_number_', type = int, default = 8192, help = 'nsamples for SDR')
parser.add_argument('-b', dest = 'block_number_', type = int, default = 20, help = 'nblocks for SDR')
parser.add_argument('-t', dest = 'tone_number_', type = float, default = .2e6, help = 'Frequency being sampled in MHz')
parser.add_argument('-u', dest = 'time_number_', type = int, default = 60, help = 'Amount of time between sampling frequency changes in seconds')

args = parser.parse_args()
file_number = args.file_number_
fs_number = args.fs_number_ * 1e6
sample_number = args.sample_number_
block_number = args.block_number_
tone_number = args.tone_number_ * 1e6
file_number = str(file_number) + '/'
time_number = args.time_number_



files(file_number)
blocks = block_number
tone = tone_number
fs = fs_number
samples = sample_number
beginning = 0
end = samples*blocks
wait = time_number

file_counter = 0
num = 0
limit = 100

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)
dac.raw_value = 0
sdr = ugradio.sdr.SDR(sample_rate = fs, direct=True)

dac_values = []
wave_values = []
df_values = []
unix_values = []

###

offset = 10

while offset > .4:
    print('Locking')
    data = sdr.capture_data(nsamples=samples,nblocks=blocks)
    data = np.concatenate(data)
    amount = data.size
    offset = SDR_Test.receive_sync_test30.receive_fitting(data, amount, beginning, end, f_sample = sdr.get_sample_rate(), tone = tone)
    beginning += amount
    end += amount
    changing = SDR_Test.receive_sync_test30.receive_sync(offset)
    dac.raw_value += int(changing)
    lock_time = time.time()
    dac_values.append(dac.raw_value)
    wave_values.append(data)
    df_values.append(offset)
    unix_values.append(lock_time)
    
    
    num += 1
    print(num)
    if num == limit:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            
        np.save('/home/radiopi/sync_data/sdr/pause/dac_values' + file_number + f'/dac_values_{timestamp}', np.array(dac_values))
        np.save('/home/radiopi/sync_data/sdr/pause/d_f_values' + file_number + f'/d_f_values_{timestamp}', np.array(df_values))
        np.save('/home/radiopi/sync_data/sdr/pause/wave_values' + file_number + f'/wave_values{timestamp}', np.array(wave_values))
        np.save('/home/radiopi/sync_data/sdr/pause/unix_values' + file_number + f'/unix_values_{timestamp}', np.array(unix_values))
        print(f'saved on {timestamp}')    
        print('saved!')
        
        dac_values = []
        wave_values = []
        df_values = []
        unix_values = []
        num = 0
        file_counter += 1
        print('Number of times saved:', file_counter)


###
print('Locking ended, waiting 60 seconds to sync...')

start_time = time.time()
end_time = time.time()

while True:
    data = sdr.capture_data(nsamples=samples,nblocks=blocks)
    data = np.concatenate(data)
    amount = data.size
    df = SDR_Test.receive_sync_test30.receive_fitting(data, amount, beginning, end, f_sample = sdr.get_sample_rate(), tone = tone)
    beginning += amount
    end += amount
    if end_time - start_time > wait:
        changing = SDR_Test.receive_sync_test30.receive_sync(df)
        dac.raw_value += int(changing)
        start_time = time.time()
        print('Adjusted DAC')
    
    end_time = time.time()
    dac_values.append(dac.raw_value)
    wave_values.append(data)
    df_values.append(df)
    unix_values.append(end_time)
    
    
    num += 1
    print(num)
    if num == limit:
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            
        np.save('/home/radiopi/sync_data/sdr/pause/dac_values' + file_number + f'/dac_values_{timestamp}', np.array(dac_values))
        np.save('/home/radiopi/sync_data/sdr/pause/d_f_values' + file_number + f'/d_f_values_{timestamp}', np.array(df_values))
        np.save('/home/radiopi/sync_data/sdr/pause/wave_values' + file_number + f'/wave_values{timestamp}', np.array(wave_values))
        np.save('/home/radiopi/sync_data/sdr/pause/unix_values' + file_number + f'/unix_values_{timestamp}', np.array(unix_values))
        print(f'saved on {timestamp}')    
        print('saved!')
        
        dac_values = []
        wave_values = []
        df_values = []
        unix_values = []
        num = 0
        file_counter += 1
        print('Number of times saved:', file_counter)
