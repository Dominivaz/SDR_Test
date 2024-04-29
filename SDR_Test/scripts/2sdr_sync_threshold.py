import numpy as np
import ugradio
import SDR_Test
import datetime
import time
import board
import busio
import adafruit_mcp4725
import threading
import matplotlib.pyplot as plt
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

parser = ArgumentParser(description = 'files', formatter_class = ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', dest = 'file_number_', type = int, help = 'File number for data')
parser.add_argument('-n', dest = 'fs_number_', type = float, default = 2.2, help = 'Sampling frequency for SDR in MHz')
parser.add_argument('-s', dest = 'sample_number_', type = int, default = 8192, help = 'nsamples for SDR')
parser.add_argument('-b', dest = 'block_number_', type = int, default = 20, help = 'nblocks for SDR')
parser.add_argument('-t', dest = 'tone_number_', type = float, default = .2, help = 'Frequency being sampled in MHz')
parser.add_argument('-p', dest = 'phase_number_', type = float, default = 2, help = 'Max and min phase difference allowed before syncing in Hz')
parser.add_argument('-x', dest = 'sync_number_', type = int, default = 1, help = 'Options for the SI chip to sync to - 1:SDR 2:wave 3:no sync')


args = parser.parse_args()
file_number = args.file_number_
fs_number = args.fs_number_ * 1e6
sample_number = args.sample_number_
block_number = args.block_number_
tone_number = args.tone_number_ * 1e6
file_number = str(file_number) + '/'
phase_number = args.phase_number_
sync_number = args.sync_number_

class match:
    def __init__(self, sample_rate, loops, nsamples, tone, file_number, sync_number):
        self.sample_rate = sample_rate
        self.loops = loops
        self.nsamples = nsamples
        self.tone = tone
        self.sdr_normal = ugradio.sdr.SDR(device_index=1, sample_rate = self.sample_rate, direct=True)
        self.sdr_SI = ugradio.sdr.SDR(device_index=0, sample_rate = self.sample_rate, direct=True)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.dac = adafruit_mcp4725.MCP4725(self.i2c)
        self.file_number = str(file_number)+'/'
        self.sync_number = sync_number
        self.dac.raw_value = 0
        self.dac_values = []
        self.wave_values_normal = []
        self.wave_values_SI = []
        self.d_f_values = []
        self.normal_df_value = []
        self.SI_df_value = []
        self.number = 0
        self.start_normal = 0
        self.stop_normal = self.nsamples*self.loops
        self.start_SI = 0
        self.stop_SI = self.nsamples*self.loops
        
        
    def capture_normal(self):
        self.thrd = threading.Thread(target = self.capture_SI())
        self.thrd.start()
        print('Capturing Normal Data...')
        self.data_normal = self.sdr_normal.capture_data(nsamples=self.nsamples, nblocks=self.loops)
        self.data_normal = np.concatenate(self.data_normal)
        self.amount = self.data_normal.size
        self.normal_df = SDR_Test.receive_sync_test30.receive_fitting(self.data_normal, self.amount, self.start_normal, self.stop_normal, f_sample = self.sdr_normal.get_sample_rate(), tone = self.tone)
        self.start_normal += self.amount
        self.stop_normal += self.amount
        
        print('Normal Data Captured...')
        print('Normal df:', self.normal_df)
        self.wave_values_normal.append(self.data_normal)
        
    def capture_SI(self):
        print('Capturing SI Data')
        SI_df_ave = []
        self.data_SI = self.sdr_SI.capture_data(nsamples=self.nsamples, nblocks=self.loops)
        self.data_SI = np.concatenate(self.data_SI)
        self.amount = self.data_SI.size
        self.SI_df = SDR_Test.receive_sync_test30.receive_fitting(self.data_SI, self.amount, self.start_SI, self.stop_SI, f_sample = self.sdr_SI.get_sample_rate(), tone = self.tone)
        self.start_SI += self.amount
        self.stop_SI += self.amount

        print('SI Data Captured...')
        print('SI df:', self.SI_df)
        self.wave_values_SI.append(self.data_SI)
        
    def lock(self):
        if self.sync_number == 1:
            df = (self.SI_df - self.normal_df)
        if self.sync_number == 2:
            df = self.SI_df
        if self.sync_number == 3:
            df = 0
        print('df Difference:', df)
        changing = SDR_Test.receive_sync_test30.receive_sync(df)
        print('Changing:', changing)
        self.dac.raw_value += int(changing)
        return df
        
    def drift(self):
        if self.sync_number == 1:
            df = (self.SI_df - self.normal_df)
        if self.sync_number == 2:
            df = self.SI_df
        if self.sync_number == 3:
            df = 0
        print('df Difference:', df)
        changing = SDR_Test.receive_sync_test30.receive_sync(df)
        print('Changing:', changing)
        self.dac.raw_value += int(changing)
        
        
        self.normal_df_value.append(self.normal_df)
        self.SI_df_value.append(self.SI_df)
        self.dac_values.append(self.dac.raw_value)
        print('Appended df Values...')
        self.number += 1
        print(self.number)
        
    def files(self):
        os.mkdir('/home/radiopi/sync_data/2sdr/dac_2sdr_test' + self.file_number)
        os.mkdir('/home/radiopi/sync_data/2sdr/d_f_values_2sdr_test' + self.file_number)
        os.mkdir('/home/radiopi/sync_data/2sdr/wave_data_2sdr_normal_test' + self.file_number)
        os.mkdir('/home/radiopi/sync_data/2sdr/wave_data_2sdr_SI_test' + self.file_number)
        os.mkdir('/home/radiopi/sync_data/2sdr/d_f_individual_2sdr_normal_test' + self.file_number)
        os.mkdir('/home/radiopi/sync_data/2sdr/d_f_individual_2sdr_SI_test' + self.file_number)
        
       
    def save(self):
        if self.number == 100:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            
            np.save('/home/radiopi/sync_data/2sdr/dac_2sdr_test' + self.file_number + f'/dac_values_{timestamp}', np.array(self.dac_values))
            np.save('/home/radiopi/sync_data/2sdr/d_f_values_2sdr_test' + self.file_number + f'/d_f_values_{timestamp}', np.array(self.d_f_values))
            np.save('/home/radiopi/sync_data/2sdr/wave_data_2sdr_normal_test' + self.file_number + f'/wave_values_normal_{timestamp}', np.array(self.wave_values_normal))
            np.save('/home/radiopi/sync_data/2sdr/wave_data_2sdr_SI_test' + self.file_number + f'/wave_values_SI_{timestamp}', np.array(self.wave_values_SI))
            np.save('/home/radiopi/sync_data/2sdr/d_f_individual_2sdr_normal_test' + self.file_number + f'/2df_values_normal_{timestamp}', np.array(self.normal_df_value))
            np.save('/home/radiopi/sync_data/2sdr/d_f_individual_2sdr_SI_test' + self.file_number + f'/2df_values_SI_{timestamp}', np.array(self.SI_df_value))
            print(f'saved on {timestamp}')
            
            print('saved!')
            self.dac_values = []
            self.wave_values_normal = []
            self.wave_values_SI = []
            self.d_f_values = []
            self.normal_df_value = []
            self.SI_df_value = []
            self.number = 0
            
    def stop(self):
        self.thrd.join()
        
        
        
if __name__ == "__main__":
    sync2 = match(sample_rate=fs_number, loops=block_number, nsamples=sample_number, tone=tone_number, file_number=file_number)
    sync2.files()
    print('Everything initialized...')
    try:
        print('Starting loop...')
        print('Getting initial phase difference...')
        threshold = phase_number
        sync2.capture_normal()
        difference = sync2.lock()
        while difference > threshold:
            print('Locking before applying threshold...')
            sync2.capture_normal()
            difference = sync2.lock()
        print('locked...')
        while True:
            sync2.capture_normal()
            sync2.drift()
            sync2.save()
    except(KeyboardInterrupt):
        sync2.stop()
        print('Sync2 Stopped...')
    finally:
        print('done')
