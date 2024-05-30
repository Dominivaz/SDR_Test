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
    """
    Creates file directory
    
    Parameters:
    file_number (int): Number to name file in the directory
    
    """
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/dac_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/d_f_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/wave_values' + file_number)
    os.mkdir('/home/radiopi/sync_data/sdr/threshold/unix_values' + file_number)
    
def sampling(nsamples, nblocks, tone, start, stop):
    """
    Samples and concatenates data, calculates difference frequency, then adds to time for simulated wave
    
    Parameters:
    nsamples (int): Number of samples from SDR
    nblocks (int): Number of blocks from SDR
    tone (float): Known frequency from injected signal
    start (int): Sample number that the simulated wave starts with
    stop (int): sample number that the simulated ends with
    
    Returns:
    df (float): difference frequency calculated from receive_fitting function
    data (list): Compiled data sampled from SDR
    
    """
    data = sdr.capture_data(nsamples=nsamples,nblocks=nblocks)
    data = np.concatenate(data)
    amount = data.size
    df = SDR_Test.receive_sync_test30.receive_fitting(data, amount, start, stop, f_sample = sdr.get_sample_rate(), tone = tone)
    start += amount
    stop += amount
    return df, data

def DAC_change(diff):
    """
    Converts difference frequency to bit values using receive_sync function, then adds those changes to DAC bits
    Total bits have to be between 0 and 4095, errors occur otherwise
    
    Parameters:
    diff (float): Difference frequency calculated between 2 clock sources
    
    """
    changing = SDR_Test.receive_sync_test30.receive_sync(diff)
    dac.raw_value += int(changing)
    print(dac.raw_value)
    
def appending(data, diff, time): ### uses global variables, will change later
    """
    Appends sampled data, dac, unix, and difference frequency values to be saved
    
    Parameters:
    data (list): Sampled data from SDR
    diff (list): Calculated difference frequencies
    time (list): Unix times
    
    """
    dac_values.append(dac.raw_value)
    wave_values.append(data)
    df_values.append(diff)
    unix_values.append(time)
    
def save(dac_values, df_values, wave_values, unix_values):
    """
    Saves currently appended DAC, difference frequency, sampled data, and unix values
    
    Parameters:
    dac_values (list): List of bit values DAC is set to
    df_values (list): List of difference frequencies
    wave_values (list): List of data sampled from SDR
    unix_values (list): List of unix values
    
    """
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
        
    np.save('/home/radiopi/sync_data/sdr/threshold/dac_values' + file_number + f'/dac_values_{timestamp}', np.array(dac_values))
    np.save('/home/radiopi/sync_data/sdr/threshold/d_f_values' + file_number + f'/d_f_values_{timestamp}', np.array(df_values))
    np.save('/home/radiopi/sync_data/sdr/threshold/wave_values' + file_number + f'/wave_values{timestamp}', np.array(wave_values))
    np.save('/home/radiopi/sync_data/sdr/threshold/unix_values' + file_number + f'/unix_values_{timestamp}', np.array(unix_values))
    print(f'saved on {timestamp}')    
    print('saved!')
    

    
# Parser settings for terminal
    
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

# Initializing i2c, DAC, SDR, and setting limits for saving

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

# Collecting current difference frequency
offset = sampling(samples,blocks,tone,beginning,end)

while offset[0] > .4:
    
    # While loop that attempts to phaselock sdr clock to tone until the 
    #difference frequency calculated is bellow .4 Hz, the smallest change 
    #change that the DAC is capable of
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
    # While loop that calculates difference frequency between the tone and sample frequency
    #of the SDR, then changes clock frequency if the difference frequency
    #reaches a specified value from terminal. If the difference frequency is smaller than
    #the specified value, no changes will be done to the DAC.
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
