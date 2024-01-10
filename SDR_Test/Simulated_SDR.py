class SDR:
    def __init__(self, sample_freq, sample_rate):
        self.sample_freq = sample_freq
        self.sample_rate = sample_rate
    
    def hello(self):#
        print('hello')#
        
    def data(self):
        ntimes = np.linspace(0, 1, 12288)
#         self.tone = tone
#         self.freq = freq
#         self.time = np.arange(ntimes)/self.sample_freq
        self.sin = np.sin(2*np.pi*self.sample_freq*ntimes)
        return self.sin
#         sample = int(np.round(sample_freq/sample_rate))
#         print(sample)
#         return sin[::sample]
    
    def capture(self):
        sample = int(np.round(self.sample_freq/self.sample_rate))
        print(sample)
        x = self.data()
        print(x.shape)
        return x[::sample]
    
#     def sample(self, freq):
#         sampling_freq = signal_freq/2
#         data = wave[::6]
#         return
        
n1 = SDR(28.8e6, 3.2e6)
print(n1.sample_freq)
print(n1.sample_rate)
n1.hello()
n1.capture()