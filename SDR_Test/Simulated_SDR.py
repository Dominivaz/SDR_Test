import numpy as np

class SDR:
    def __init__(self, sample_freq, sample_rate, nblocks):
        self.sample_freq = sample_freq
        self.sample_rate = sample_rate
        self.nblocks = nblocks
    
    def hello(self):#
        print('hello')#
        
    def data(self):
        ntimes = np.linspace(0, 1, 12288)
        self.sin = np.sin(2*np.pi*self.sample_freq*ntimes)
        return self.sin
    
    def capture(self):
        blocks = []
        sample = int(np.round(self.sample_freq/self.sample_rate))
        print(sample)
        for i in range(self.nblocks):
            x = self.data()
            blocks.append(x)
        blocks = np.array(blocks)
        return blocks[:,::sample]