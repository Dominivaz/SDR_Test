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
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/dac_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/d_f_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/wave_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/unix_values' + file_number)
    
def sampling(nsamples, nblocks, tone, start, stop):
    data = sdr.capture_data(nsamples=nsamples,nblocks=nblocks)
    data = np.concatenate(data)
    amount = data.size
    df = SDR_Test.receive_sync_test30.receive_fitting(data, amount, start, stop, f_sample = sdr.get_sample_rate(), tone = tone)
    start += amount
    stop += amount
    return df, data

def DAC_change(diff):
    changing = SDR_Test.receive_sync_test30.receive_sync(diff)
    dac.raw_value += int(changing)
    print(dac.raw_value)
    
def appending(data, diff, time):
    dac_values.append(dac.raw_value)
    wave_values.append(data)
    df_values.append(diff)
    unix_values.append(time)
    
def save(dac_values, df_values, wave_values, unix_values):
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        
    np.save('/home/radiopi/sync_data/sdr/threshold/dac_values' + file_number + f'/dac_values_{timestamp}', np.array(dac_values))
    np.save('/home/radiopi/sync_data/sdr/threshold/d_f_values' + file_number + f'/d_f_values_{timestamp}', np.array(df_values))
    np.save('/home/radiopi/sync_data/sdr/threshold/wave_values' + file_number + f'/wave_values{timestamp}', np.array(wave_values))
    np.save('/home/radiopi/sync_data/sdr/threshold/unix_values' + file_number + f'/unix_values_{timestamp}', np.array(unix_values))
    print(f'saved on {timestamp}')    
    print('saved!')
    

    
parser = ArgumentParser(description = 'files', formatter_class = ArgumentDefaultsHelpFormatter)

parser.add_argument('-f', dest = 'file_number_', type = int, help = 'File number for data')
parser.add_argument('-n', dest = 'fs_number_', type = float, default = 2.2, help = 'Sampling frequency for SDR in MHz')
parser.add_argument('-s', dest = 'sample_number_', type = int, default = 8192, help = 'nsamples for SDR')
parser.add_argument('-b', dest = 'block_number_', type = int, default = 20, help = 'nblocks for SDR')
parser.add_argument('-t', dest = 'tone_number_', type = float, default = .2, help = 'Frequency being sampled in MHz')
parser.add_argument('-p', dest = 'phase_number_', type = float, default = 2, help = 'Max and min phase difference allowed before syncing in Hz')

args = parser.parse_args()
file_number = args.file_number_
fs_number = args.fs_number_ * 1e6
sample_number = args.sample_number_
block_number = args.block_number_
tone_number = args.tone_number_ * 1e6
file_number = str(file_number) + '/'
phase_number = args.phase_number_



files(file_number)
blocks = block_number
tone = tone_number
fs = fs_number
samples = sample_number
beginning = 0
end = samples*blocks
threshold = phase_number

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

offset = sampling(samples,blocks,tone,beginning,end)

while offset[0] > .4:
    print('Locking')
    offset = sampling(samples,blocks,tone,beginning,end)
    DAC_change(offset[0])
    lock_time = time.time()
    appending(offset[1], offset[0],lock_time)
    num += 1
    print(num)
    if num == limit:
        save(dac_values,df_values,wave_values,unix_values)
        dac_values = []
        wave_values = []
        df_values = []
        unix_values = []
        num = 0
        file_counter += 1
        print('Number of times saved:', file_counter)


###
print('Locking ended, waiting for '+ str(threshold) +' phase difference...')

start_time = time.time()
end_time = time.time()

while True:
    df = sampling(samples,blocks,tone,beginning,end)
    if abs(df[0]) > threshold:
        DAC_change(df[0])
        start_time = time.time()
        print('Adjusted DAC')
    end_time = time.time()
    appending(df[1], df[0], end_time)
    num += 1
    print(num)
    if num == limit:
        save(dac_values,df_values,wave_values,unix_values)
        dac_values = []
        wave_values = []
        df_values = []
        unix_values = []
        num = 0
        file_counter += 1
        print('Number of times saved:', file_counter)
