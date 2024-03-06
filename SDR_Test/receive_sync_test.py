import numpy as np
import matplotlib.pyplot as plt

def receive_fitting(x, ntimes, start, stop, f_sample=28.8e6, tone=1e6, pad=8):
    
    t = np.arange(start, stop)/f_sample
    lo = np.cos(2*np.pi*t*tone)-1j*np.sin(2*np.pi*t*tone)#
    wave = x[300:-300]
    z = wave*lo[300:-300]#
    #z = np.array(z) #unnecessary?

    mw = z.copy()
    #mw = np.mean(mw, axis =0)
    
    xfft = (np.fft.fft(mw))
    xfft[pad+1:-pad] = 0
    mw = np.fft.ifft(xfft)

    mw /= np.abs(mw)
    
    FREQS_z = ((np.fft.fftfreq(mw.size, np.median(np.diff(t)))/1))
        
    y = 2*np.pi*tone
    mw_fft = (np.fft.fft(mw))
    i = np.argmax(np.abs(mw_fft))
    print('i:', i)
    
    
    if i != 0:
        print('broke')
        return 0
        #plt.figure()
        #plt.plot(lo, label = 'lo')
        #plt.plot(wave, label = 'wave')
        #plt.plot(z, label = 'mixed')
        #plt.show()
        #reset = (np.conjugate(mw_fft[0])/np.abs(mw_fft[0]))#
        
        #d_f = (f_sample/(tone))*FREQS_z[i]
        #return d_f
    else:
        reset = (np.conjugate(mw_fft[i])/np.abs(mw_fft[i]))
        big = ((reset)*(mw))
#         slope = np.polyfit(t, big.imag, 1)[0]
        #slope = np.polyfit(t[250:-250], big.imag[250:-250], 1)[0]
        slope, intercept = np.polyfit(t[300:-300], big.imag, 1)
        #plt.figure()
        #plt.plot(t[300:-300], big.imag)
        #plt.plot(t[300:-300], slope*t[300:-300]+intercept)
        #plt.show()
        d_f = (slope*f_sample)/(y-slope)
        print(f'{d_f=}')
        return d_f

    
    
# f_sample = 10e6 'our gps reference'

def receive_sync(d_f):
    diff = 3.0393
    changing = np.round((d_f/diff))
    return changing
