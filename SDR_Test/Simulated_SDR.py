class SDR:
    def __init__(self, sample_freq, sample_rate):
        self.sample_freq = sample_freq
        self.sample_rate = sample_rate
    
    def hello(self):#
        print('hello')#
        
    def data(self):
        ntimes = np.linspace(0, 1, 12288)
        self.sin = np.sin(2*np.pi*self.sample_freq*ntimes)
        return self.sin
    
    def capture(self):
        sample = int(np.round(self.sample_freq/self.sample_rate))
        print(sample)
        x = self.data()
        print(x.shape)
        return x[::sample]