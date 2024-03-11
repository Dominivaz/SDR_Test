import numpy as np
import matplotlib.pyplot as plt

def receive_fitting(x, ntimes, start, stop, f_sample=28.8e6, tone=1e6, pad=8, shave=300):
    
    t = np.arange(start, stop)/f_sample
    y = 2*np.pi*tone
    lo = np.cos(y*t)-1j*np.sin(y*t)#
    wave = x[shave:-shave]
    mw = wave*lo[shave:-shave]#

    #mw = z.copy()
    #mw = np.mean(mw, axis =0)
    
    mw_fft = (np.fft.fft(mw))
    mw_fft[pad+1:-pad] = 0
    i = np.argmax(np.abs(mw_fft))
    mw = np.fft.ifft(mw_fft)

    mw /= np.abs(mw)
    
    FREQS_z = ((np.fft.fftfreq(mw.size, np.median(np.diff(t)))/1))
        
    #i = np.argmax(np.abs(mw_fft))
    print('i:', i)
    
    
    if i != 0:
        print('broke')
        return 0
        #reset = (np.conjugate(mw_fft[0])/np.abs(mw_fft[0]))#
        
        #d_f = (f_sample/(tone))*FREQS_z[i]
        #return d_f
    else:
        reset = (np.conjugate(mw_fft[i])/np.abs(mw_fft[i]))
        big = ((reset)*(mw))
        slope, intercept = np.polyfit(t[shave:-shave], big.imag, 1)
        d_f = (slope*f_sample)/(y-slope)
        print(f'{d_f=}')
        return d_f

    
    
# f_sample = 10e6 'our gps reference'

def receive_sync(d_f):
    max_freq = 28801126
    min_freq = 28799479
    #max_freq = 28800979
    #min_freq = 28799812
    freq_range = max_freq-min_freq
    bit_amount = 4096
    #bit_amount = 3276
    diff = freq_range/bit_amount
    changing = np.round((d_f/diff))
    return changing
