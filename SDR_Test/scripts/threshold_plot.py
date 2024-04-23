import numpy as np
import matplotlib.pyplot as plt
import glob
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


parser = ArgumentParser(description = 'plot', formatter_class = ArgumentDefaultsHelpFormatter)
parser.add_argument('-f', dest = 'file_number', type = int, help = 'File number to plot')
parser.add_argument('-c', dest = 'cut_', type = int, help = 'Index to start from for DAC values')

parser.add_argument('--p1', action = 'store_true', help = 'Display plot: df values')
parser.add_argument('--p2', action = 'store_true', help = 'Display plot: DAC values')
parser.add_argument('--p3', action = 'store_true', help = 'Display plot: frequency calculation')
parser.add_argument('--p4', action = 'store_true', help = 'Display plot: unix vs df')
parser.add_argument('--p5', action = 'store_true', help = 'Display plot: unix vs DAC')
parser.add_argument('--p6', action = 'store_true', help = 'Display plot: unix vs frequency calculation')
parser.add_argument('--p7', action = 'store_true', help = 'Display plot: seconds vs df')
parser.add_argument('--p8', action = 'store_true', help = 'Display plot: seconds vs DAC')
parser.add_argument('--p9', action = 'store_true', help = 'Display plot: seconds vs frequency calculation')

args = parser.parse_args()
direct = f'{args.file_number}/*'
cut = args.cut_


df_list =     sorted(glob.glob('/home/radiopi/sync_data/sdr/threshold/d_f_values' + direct), reverse=False)
dac_list =    sorted(glob.glob('/home/radiopi/sync_data/sdr/threshold/dac_values' + direct), reverse=False)
unix_list =   sorted(glob.glob('/home/radiopi/sync_data/sdr/threshold/unix_values' + direct), reverse=False)




df_array = []
dac_array = []
unix_array = []





for i in df_list:
	data = np.load(i)
	df_array.append(data)

for i in dac_list:
	data = np.load(i)
	dac_array.append(data)

for i in unix_list:
    data = np.load(i)
    unix_array.append(data)



print('array shape:', np.array(df_array).shape)

df = np.concatenate(df_array, axis = 0)

dac = np.concatenate(dac_array, axis = 0)
unix = np.concatenate(unix_array, axis = 0)



print('si:', df.shape)

print('df average:', np.mean(df[80:]))
print('df std:', np.std(df[80:]))


max_freq = 28801126
min_freq = 28799479
freq_range = max_freq-min_freq
bit_amount = 4096
diff = freq_range/bit_amount

f_sample_prime = diff*dac[cut:] + min_freq

seconds_ = unix[-1] - unix[0]
seconds = np.linspace(0, seconds_, len(unix))

print('Sampled for:' + seconds_ + 'seconds')

if args.p1:
    plt.figure()
    plt.plot(df, label = 'df')
    plt.legend()
    plt.ylabel('Calculated df from 2.2 MHz')
    plt.xlabel('Counts')
    plt.show()


if args.p2:
    plt.figure()
    plt.plot(dac[cut:], label = 'DAC Values')
    plt.legend()
    plt.xlabel('Counts')
    plt.ylabel('Bits')
    plt.show()

if args.p3:
    plt.figure()
    plt.plot(f_sample_prime, label = 'DAC to Freq Values')
    plt.legend()
    plt.xlabel('Counts')
    plt.ylabel('Calculated Clock Frequency')
    plt.show()
    
if args.p4:
    plt.figure()
    plt.plot(unix, df, label = 'df')
    plt.legend()
    plt.xlabel('Unix')
    plt.ylabel('Calculated df from 2.2 MHz')
    plt.show()
    
if args.p5:
    plt.figure()
    plt.plot(unix[cut:], dac[cut:], label = 'Dac')
    plt.legend()
    plt.xlabel('Unix')
    plt.ylabel('Bits')
    plt.show()

if args.p6:
    plt.figure()
    plt.plot(unix[cut:], f_sample_prime, label = 'df')
    plt.legend()
    plt.xlabel('Unix')
    plt.ylabel('Calculated Clock Frequency')
    plt.show()
    
if args.p7:
    plt.figure()
    plt.plot(seconds, df, label = 'df')
    plt.legend()
    plt.xlabel('Seconds')
    plt.ylabel('Calculated df from 2.2 MHz')
    plt.show()
    
if args.p8:
    plt.figure()
    plt.plot(seconds[cut:], dac[cut:], label = 'Dac')
    plt.legend()
    plt.xlabel('Seconds')
    plt.ylabel('Bits')
    plt.show()

if args.p9:
    plt.figure()
    plt.plot(seconds[cut:], f_sample_prime, label = 'df')
    plt.legend()
    plt.xlabel('Seconds')
    plt.ylabel('Calculated Clock Frequency')
    plt.show()
