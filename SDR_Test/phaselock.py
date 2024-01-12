import numpy as np
import ugradio
import SDR_Test
import datetime
import time
import board
import busio
import adafruit_mcp4725

print('Started Script...')

f_sample_prime = 28.8e6

sdr = ugradio.sdr.SDR(sample_rate = 3.2e6)

i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

dac.raw_value = 2010

print('Everything Initialized...')

dac_values = []

save = 0

sdr.capture_data
sdr.capture_data
print('Cleaned SDR...')

try:
    
    while True:
        data = sdr.capture()
        print('Captured Data...')
        d_f = SDR_Test.receive_sync.receive_fitting(data, data.shape[1], f_sample = 28.8e6, tone = 1e6)
        changing = SDR_Test.receive_sync.receive_sync(d_f)
        dac.raw_value += changing
        print('changing:', g)
        print('f_sample_prime:', dac.raw_value)
        dac_values.append(dac.raw_value)
        save += 1
        if save == 10:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            print(f'saved on {timestamp}')
            np.save(f'/home/radiopi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
            print('saved!')
            dac_values = []
            save -= 10
except KeyboardInterrupt:
    print('Closing Connections and Saving Last Iteration...')
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
    np.save(f'/home/radiopi/dac_values/data/dac_values_{timestamp}', np.array(dac_values))
    print('Saved Last Iteration...')
    conn.close()
    receiver_socket_close()
    print('Done!')