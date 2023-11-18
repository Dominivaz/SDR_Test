def receive_fitting(x, f_sample=10e6, ntimes=2048, tone=1e6):
    
    t = np.arange(ntimes)/f_sample
    x = np.array(x) #unnecessary?

    mw = x.copy()
    mw = np.mean(mw, axis =0)
    
    xfft = (np.fft.fft(mw))
    xfft[pad+1:-pad] = 0
    mw = np.fft.ifft(xfft)

    mw /= np.abs(mw)
    FREQS_z = ((np.fft.fftfreq(mw.size, np.median(np.diff(t)))/1))
        
    y = 2*np.pi*tone
    mw_fft = (np.fft.fft(mw))
    i = np.argmax(np.abs(mw_fft))
    
    if i != 0:
        d_f = (f_sample/(tone))*FREQS_z[i]
        return d_f
    else:
        reset = (np.conjugate(mw_fft[i])/np.abs(mw_fft[i]))
        big = ((reset)*(mw))
        slope = np.polyfit(t[250:-250], big.imag[250:-250], 1)[0]
        d_f = (slope*f_sample)/(y-slope)
        return d_f

    
    
# f_sample = 10e6 'our gps reference'

def receive_sync(d_f):
    diff = 3.0393
    changing = np.round((d_f/diff))
    return changing