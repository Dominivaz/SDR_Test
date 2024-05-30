import numpy as np
import matplotlib.pyplot as plt

def receive_fitting(x, ntimes, start, stop, f_sample=28.8e6, tone=1e6, pad=8, shave=300):
    """
    Function that calculates the difference frequency between a known signal and an SDR sampled signal.
    
    Parameters:
    x (array): Data sampled from an SDR
    ntimes (int): Size of simulated wave, must match size of x
    start (int): Sample number to start simulated wave from
    stop (int): Sample number to stop simulated wave at
    f_sample (float): Sample frequency SDR is set to
    tone (float): Frequency of injected signal
    pad (int): Size of filter away from the 0th index of fft
    shave (int): Amount of samples to remove from beginning and end of mixed wave
    
    Returns:
    d_f (float): Calculated difference frequency
    
    Simulates an injected known tone with a given sample frequency, then mixes that wave with the sampled 
    tone from an SDR. The sum frequency is removed from the fft of the mixed signal, 
    then the location of the difference frequency is recorded in fourier domain. If the difference 
    frequency is large enough to appear outside the 0th bin of the fft, then it will convert its
    index to a frequency, and directly return the frequency the spike lies on. If the difference frequency 
    is too small and falls into the 0th bin, the conjugate and absolute values of the spike are divided, 
    then multipled into the ifft of the filtered fft. A fit is then applied to the imaginary part of the 
    resulting wave, where its slope is used to calculate its difference frequency.
    
    """
    
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
        #print('broke')
        #return 0
        reset = (np.conjugate(mw_fft[0])/np.abs(mw_fft[0]))#
        
        d_f = (f_sample/(tone))*FREQS_z[i]
        print(f'{d_f=}')
        return d_f
    else:
        reset = (np.conjugate(mw_fft[i])/np.abs(mw_fft[i]))
        big = ((reset)*(mw))
        slope, intercept = np.polyfit(t[shave:-shave], big.imag, 1)
        d_f = (slope*f_sample)/(y-slope)
        print(f'{d_f=}')
        return d_f

    
    
# f_sample = 10e6 'our gps reference'

def receive_sync(d_f): ###Might add float to int conversion into function
    """
    Converts difference frequency into bit values for a DAC interacting with
    a configured 30ppm SI5351 Clock Generator
    
    Parameters:
    d_f (float): Difference frequency
    
    Returns:
    changing (float): Amount of bits to be added to DAC
    
    """
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
