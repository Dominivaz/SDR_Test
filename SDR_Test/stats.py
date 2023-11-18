import numpy as np
import matplotlib.pyplot as plt
import ugradio

def stats(x, ntimes=2048, sample_rate=3.2e6, nblocks=10):
    
    t = np.arange(ntimes)/sample_rate
    
    freqs = np.fft.fftfreq(t.size, np.median(np.diff(t)))
    
    data = x
    
    data = np.mean(data, axis=0)
    
    fft = np.fft.fft(data)
    
    plt.figure()
    plt.plot(t, data, label = 'Wave')
    plt.xlabel('Time []')
    plt.ylabel('Voltage [dB?]')
    plt.legend()
    plt.show()
    
    plt.figure()
    plt.plot(np.fft.fftshift(freqs), np.abs(np.fft.fftshift(fft)), label = 'FFT')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Voltage abs([dB])')
    plt.legend()
    plt.show()
    
    max_point = np.max(data)
    min_point = np.min(data)
    
    V_pp = max_point - min_point
    V_rms = (1/(2*np.sqrt(2)))*V_pp
    
    period = np.median(np.diff(np.where(data==np.max(data))))
    frequency = 1/period
    
    print('V_pp:', V_pp)
    print('\nV_rms:', V_rms)
    
    print('\nPeriod:', period)
    print('\nFrequency:', frequency)