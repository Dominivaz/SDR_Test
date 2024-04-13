
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


class match:
    def __init__(self, sample_rate, loops, nsamples, tone, file_number):
        self.sample_rate = sample_rate
        self.loops = loops
        self.nsamples = nsamples
        self.tone = tone
        self.sdr_normal = ugradio.sdr.SDR(device_index=1, sample_rate = self.sample_rate, direct=True)
        self.sdr_SI = ugradio.sdr.SDR(device_index=0, sample_rate = self.sample_rate, direct=True)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.dac = adafruit_mcp4725.MCP4725(self.i2c)
        self.file_number = str(file_number)+'/'
        self.dac.raw_value = 2500
        self.dac_values = []
        self.wave_values_normal = []
        self.wave_values_SI = []
        self.d_f_values = []
        self.normal_df_value = []
        self.SI_df_value = []
        self.number = 0
        self.start_normal = 0
        self.stop_normal = self.nsamples
        self.start_SI = 0
        self.stop_SI = self.nsamples
        
    def capture_normal(self):
        self.thrd = threading.Thread(target = self.capture_SI())
        self.thrd.start() # # #
        #print('Cleaning Normal SDR...')
        #self.sdr_normal.capture_data()
        #self.sdr_normal.capture_data()
        print('Capturing Normal Data...')
        normal_df_ave = []
        self.data_normal = self.sdr_normal.capture_data(nsamples=self.nsamples, nblocks=self.loops)
        for i in np.arange(1, self.loops):
            normal_df = SDR_Test.receive_sync_test30.receive_fitting(self.data_normal[i], self.data_normal[i].shape, self.start_normal, self.stop_normal, f_sample = self.sdr_normal.get_sample_rate(), tone = self.tone)
            normal_df_ave.append(normal_df)
            self.start_normal += self.nsamples
            self.stop_normal += self.nsamples
        normal_df_ave = np.array(normal_df_ave)
        self.normal_average = np.mean((normal_df_ave))
        self.std_normal = np.std((normal_df_ave))
        thresh = 1
        filtered_normal = (normal_df_ave)[abs((normal_df_ave)-self.normal_average) <= thresh * self.std_normal]
        self.normal_average = np.mean(filtered_normal)
        #self.data_normal = self.sdr_normal.capture_data(nblocks=1)
        print('Normal Data Captured...')
        print('Normal average df:', self.normal_average)
        self.wave_values_normal.append(self.data_normal)
        
    def capture_SI(self):
        #print('Cleaning SI SDR...')
        #self.sdr_SI.capture_data()
        #self.sdr_SI.capture_data()
        print('Capturing SI Data')
        SI_df_ave = []
        self.data_SI = self.sdr_SI.capture_data(nsamples=self.nsamples, nblocks=self.loops)
        for i in np.arange(1, self.loops):
            SI_df = SDR_Test.receive_sync_test30.receive_fitting(self.data_SI[i], self.data_SI[i].shape, self.start_SI, self.stop_SI, f_sample = self.sdr_SI.get_sample_rate(), tone = self.tone)
            SI_df_ave.append(SI_df)
            self.start_SI += self.nsamples
            self.stop_SI += self.nsamples
        SI_df_ave = np.array(SI_df_ave)
        self.SI_average = np.mean((SI_df_ave))
        self.std_SI = np.std((SI_df_ave))
        thresh = 1
        filtered_SI = (SI_df_ave)[abs((SI_df_ave)-self.SI_average) <= thresh * self.std_SI]
        self.SI_average = np.mean(filtered_SI)
        #self.data_SI = self.sdr_SI.capture_data(nblocks=1)
        print('SI Data Captured...')
        print('SI average df:', self.SI_average)
        self.wave_values_SI.append(self.data_SI)
        
    def mixing(self):
        self.thrd1 = threading.Thread(target = self.drift())
        d_f = mix_calc(self.data_SI[0], self.data_normal[0], self.data_SI.shape, f_sample = self.sdr_SI.get_sample_rate(), tone = .2e6)
        changing = SDR_Test.receive_sync.receive_sync(d_f)
        print('change:', changing)
        self.dac.raw_value += int(changing)
        print('Frequency Difference:', d_f)
        print('Changing DAC value by:', changing)
        self.d_f_values.append(d_f)
        self.dac_values.append(self.dac.raw_value)
        #plt.figure()
        #plt.plot(self.data_normal[0])
        #plt.plot(self.data_SI[0])
        #plt.show()
        self.number += 1
        
    def drift(self):
        df = (self.SI_average - self.normal_average)
        #diff = self.SI_average
        #diff = 0
        print('df Difference:', df)
        changing = SDR_Test.receive_sync_test30.receive_sync(df)
        print('Changing:', changing)
        self.dac.raw_value += int(changing)
        #print('normal df:', normal_df)
        #print('SI df:', SI_df)
        
        
        self.normal_df_value.append(self.normal_average)
        self.SI_df_value.append(self.SI_average)
        self.dac_values.append(self.dac.raw_value)
        print('Appended df Values...')
        print('Wave_values_SI shape:', np.array(self.wave_values_SI).shape)
        self.number += 1
        
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
        #self.thrd1.join()
        
        
        
if __name__ == "__main__":
    parser = ArgumentParser(description = 'files', formatter_class = ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', dest = 'file_number_', type = int, help = 'number')
    args = parser.parse_args()
    direct = args.file_number_
    sync2 = match(sample_rate=2.2e6, loops=20, nsamples=8192, tone=.2e6, file_number=direct)
    sync2.files()
    print('Everything initialized...')
    try:
        print('Starting loop...')
        while True:
            sync2.capture_normal()
            sync2.drift()
            sync2.save()
            #time.sleep(1)
    except(KeyboardInterrupt):
        sync2.stop()
        print('Sync2 Stopped...')
    finally:
        print('done')
