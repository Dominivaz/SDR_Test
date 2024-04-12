import numpy as np
import matplotlib.pyplot as plt
import glob
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


parser = ArgumentParser(description = 'plot', formatter_class = ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', dest = 'file_number', type = int, help = 'File number to plot')
parser.add_argument('-c', dest = 'cut_', type = int, help = 'Index to start from for DAC values')
args = parser.parse_args()
direct = f'{args.file_number}/*'
cut = args.cut_

#normal_list = sorted(glob.glob('/home/radiopi/sync_data/sdr/large_sample/wave_values' + direct), reverse=False)
df_list =     sorted(glob.glob('/home/radiopi/sync_data/sdr/large_sample/d_f_values' + direct), reverse=False)
dac_list =    sorted(glob.glob('/home/radiopi/sync_data/sdr/large_sample/dac_values' + direct), reverse=False)
#SI_wlist =     sorted(glob.glob('/home/radiopi/sync_data/2sdr/wave_data_2sdr_SI_test' + direct), reverse=False)
#normal_wlist =     sorted(glob.glob('/home/radiopi/sync_data/2sdr/wave_data_2sdr_normal_test' + direct), reverse=False)


#normal_array = []
df_array = []
dac_array = []
#normal_warray = []
#SI_warray = []


#or i in normal_list:
#	data = np.load(i)
#	normal_array.append(data)
	
for i in df_list:
	data = np.load(i)
	df_array.append(data)
	
for i in dac_list:
	data = np.load(i)
	dac_array.append(data)
	
#for i in normal_wlist:
#	data = np.load(i)
#	normal_warray.append(data)
	
#for i in SI_wlist:
#	data = np.load(i)
#	SI_warray.append(data)
	

	
#print('array shape:', np.array(normal_array).shape)
print('array shape:', np.array(df_array).shape)

df = np.concatenate(df_array, axis = 0)
#normal_df = np.concatenate(normal_array, axis = 0)
dac = np.concatenate(dac_array, axis = 0)
#SI_wave = np.concatenate(SI_warray, axis = 0)
#normal_wave = np.concatenate(normal_warray, axis = 0)

#t = np.arange(0, 2048)/2.2e6
#tone = .2e6
#lo = np.cos(2*np.pi*t*tone)-1j*np.sin(2*np.pi*t*tone)


print('si:', df.shape)
#print('normal', normal_df.shape)

print('df average:', np.mean(df[80:]))
print('df std:', np.std(df[80:]))
#print('normal average:', np.mean(normal_df))
#print('normal std:', np.std(normal_df))

#slope, intercept = np.polyfit(np.arange(len(normal_df)), df, 1)
#fit = slope*np.arange(len(normal_df)) + intercept
#print('slope:', slope)
#print(dac)


max_freq = 28801126
min_freq = 28799479
freq_range = max_freq-min_freq
bit_amount = 4096
diff = freq_range/bit_amount

f_sample_prime = diff*dac[cut:] + min_freq


plt.figure()
plt.plot(df, label = 'df')
#plt.plot(SI_df, label = 'SI SDR Drift')
#plt.plot(normal_df-SI_df, label = 'Difference')
plt.legend()
plt.ylabel('Frequency Difference from 2.2 MHz')
plt.xlabel('Counts')
#plt.ylim(-2,2)
plt.show()

#plt.figure()
#plt.plot(normal_df, label = 'Normal SDR Drift')
#plt.plot(fit, label = 'Fitted Line')
#plt.plot(SI_df)
#plt.legend()
#plt.show()

#plt.figure()
#plt.plot(SI_df[150:], label = 'SI SDR Drift')
#plt.legend()
#plt.show()

#plt.figure()
#plt.plot(normal_wave[0][0], label = 'Normal Wave')
#plt.plot(lo*100, label = 'LO')
#plt.plot((normal_wave*lo)[0][0], label = 'Mixed Wave')
#plt.plot(SI_wave[0][0], label = 'SI Wave')
#plt.legend()
#plt.show()

#plt.figure()
#plt.plot((normal_wave*lo)[0][0], label = 'Mixed Wave')
#plt.legend()
#plt.show()

plt.figure()
plt.plot(dac[cut:], label = 'DAC Values')
plt.legend()
plt.show()

plt.figure()
plt.plot(f_sample_prime, label = 'DAC to Freq Values')
plt.legend()
plt.xlabel('Counts')
plt.ylabel('Calculated Clock Frequency')
plt.show()
