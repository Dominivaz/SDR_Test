import numpy as np
import ugradio
import SDR_Test
import datetime
import time
import board
import busio
import adafruit_mcp4725
import threading

class match:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.sdr_normal = ugradio.sdr.SDR(device_index=0, sample_rate=self.sample_rate)
        self.sdr_SI = ugradio.sdr.SDR(device_index=1, sample_rate=self.sample_rate)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.dac = adafruit_mcp4725.MCP4725(i2c)
        self.dac.raw_value = 4095
        self.dac_values = []
        self.wave_values_normal = []
        self.wave_values_SI = []
        self.d_f_values = []
        self.normal_df_value = []
        self.SI_df_value = []
        self.number = 0
        
    def capture_normal(self):
        self.thrd = threading.Thread(target = self.capture_SI)
        self.sdr_normal.capture_data()
        self.sdr_normal.capture_data()
        self.data_normal = self.sdr_normal.capture_data(nblocks=1)
        self.wave_values_normal.append(self.data_normal)
        
    def capture_SI(self):
        self.sdr_SI.capture_data()
        self.sdr_SI.capture_data()
        self.data_SI = self.sdr_SI.capture_data(nblocks=1)
        self.wave_values_SI.append(self.data_SI)
        
    def mixing(self):
        self.thrd1 = threading.Thread(target = self.drift)
        d_f = SDR_Test.sync_SDR.mix_calc(self.data_normal, self.data_SI, self.data_normal.shape[0], f_sample = 28.8e6, tone = 1e6)
        changing = SDR_Test.receive_sync.receive_sync(d_f)
        self.dac.raw_value += changing
        print('Frequency Difference:', d_f)
        print('Changing DAC value by:', changing)
        self.d_f_values.append(d_f)
        self.dac_values.append(self.dac.raw_value)
        self.number += 1
        
    def drift(self):
        normal_df = SDR_Test.receive_sync.receive_fitting(self.data_normal, self.data_normal.shape[1], f_sample = 28.8e6, tone = .2e6)
        SI_df = SDR_Test.receive_sync.receive_fitting(self.data_SI, self.data_SI.shape[1], f_sample = 28.8e6, tone = .2e6)
        self.normal_df_value.append(normal_df)
        self.SI_df_value.append(SI_df)
        
       
    def save(self):
        if self.number == 100:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            
            stack_waves = np.concatenate((np.array(self.wave_values_normal), np.array(self.wave_values_SI)))
            stack_df = np.concatenate((np.array(self.normal_df_value), np.array(self.SI_df_value)))
            stack_waves.shape = (2,2048)
            stack_df.shape = (2,2048)
            
            np.save(f'/home/radiopi/dac_values/data/dac_values_{timestamp}', np.array(self.dac_values))
            np.save(f'/home/radiopi/dac_values/data/d_f_values_{timestamp}', np.array(self.d_f_values))
            np.save(f'/home/radiopi/dac_values/data/wave_values_{timestamp}', stack_waves)
            np.save(f'/home/radiopi/dac_values/data/2df_values_{timestamp}', stack_df)
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
        self.thrd1.join()
        
        
        
if __name__ == "__main__":
    sync2 = match(sample_rate=2.2e6)
    print('Everything initialized...')
    try:
        print('Starting loop...')
        while True:
            sync2.capture_normal()
            sync2.mixing()
            sync2.save()
    except(KeyboardInterrupt):
        sync2.stop()
        print('Sync2 Stopped...')
    finally:
        print('done')