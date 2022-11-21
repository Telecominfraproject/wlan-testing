
import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os
import sys

# Exit Codes
# 0: Success
# 1: Python Error
# 2: CSV file not found
# 3: Radio disconnected before exit threshold expected RSSI; PNG will still be generated
# 4: Attempted Bandwidth HT80 used with Channel 6

parser = argparse.ArgumentParser(description='Input and output files.')
parser.add_argument('--csv', metavar='i', type=str, help='../output.csv')
parser.add_argument('--png_dir', metavar='o', type=str, help='../PNGs')
parser.add_argument('--bandwidth', metavar='b', type=int, help='20, 40, 80')
parser.add_argument('--channel', metavar='c', type=int, help='6, 36')
parser.add_argument('--antenna', metavar='a', type=int, help='0, 1, 4, 7, 8')
parser.add_argument('--path_loss_2', metavar='p', type=float, help='26.74')
parser.add_argument('--path_loss_5', metavar='q', type=float, help='31.87')

args = parser.parse_args()
CSV_FILE = args.csv
PNG_OUTPUT_DIR = args.png_dir
BANDWIDTH = args.bandwidth
CHANNEL = args.channel
ANTENNA = args.antenna
ANTENNA_LEGEND = {
    0: 'Diversity (All)',
    1: 'Fixed-A (1x1)',
    4: 'AB (2x2)',
    7: 'ABC (3x3)',
    8: 'ABCD (4x4)'
}
BASE_PATH_LOSS = 36
if CHANNEL == 6:
    BASE_PATH_LOSS = args.path_loss_2
elif CHANNEL == 36:
    BASE_PATH_LOSS = args.path_loss_5
TX_POWER = 20
CHECK_RADIOS = [0, 1, 2, 3, 4, 5, 6] # radios to check during early exit
EXIT_THRESHOLD = -85. # expected-signal cutoff for radio-disconnect exit code


# helper functions
def filt(lst): # filter out all instances of nan
    return lst[~(np.isnan(lst))]


def avg(lst): # mean
    lst = filt(lst)
    return sum(lst)/len(lst) if len(lst) else np.nan


def dev(lst): # element-wise deviation from mean (not standard deviation)
    return np.abs(avg(lst) - lst)


def expected_signal(attenuation): # theoretical expected signal
    return TX_POWER - (BASE_PATH_LOSS + attenuation)


# early exit for disconnected radio before threshold expected RSSI
def check_data(signal, signal_exp):
    if CHANNEL == 6:
        CHECK_RADIOS.remove(1) # TODO: Make generic
    if CHANNEL == 36:
        CHECK_RADIOS.remove(0) # TODO: Make generic
    threshold_ind = np.where(signal_exp <= EXIT_THRESHOLD)[0][0] # the first index where exit threshold is reached
    isnans = np.concatenate([np.isnan(e) for e in signal[0:threshold_ind, CHECK_RADIOS]]) # array of booleans
    if (any(isnans)):
        print(F'Warning: Radio disconnected before exit threshold expected RSSI; check {PNG_OUTPUT_DIR}/{CHANNEL}_{ANTENNA}_{BANDWIDTH}_*.png.')
        sys.exit(3)


# check bandwidth compatibility
if CHANNEL == 6 and BANDWIDTH == 80:
    sys.exit(4)

# read data from file
data = []
if not os.path.exists(CSV_FILE):
    sys.exit(2)
with open(CSV_FILE, 'r') as filename:
    reader = csv.reader(filename)
    for row in reader:
        data.append(row)

# populate signal and attenuation data
atten_data = [[], [], [], [], [], [], []]
signal_data = [[], [], [], [], [], [], []]
for i in range(1, len(data)):
    for j in range(0, len(atten_data)):
        if int(data[i][5]) == j:
            # attenuation data
            atten_data[j].append(float(data[i][0]))
            # signal data
            rssi = float(data[i][13])
            if rssi:
                signal_data[j].append(float(data[i][13]))
            else:
                signal_data[j].append(np.nan)

atten = np.array(atten_data).T
signal = np.array(signal_data).T
signal_avg = np.array([avg(row) for row in signal])
signal_exp = expected_signal(atten[:, 0])
signal_dev = np.array([signal[i] - signal_exp[i] for i in range(0, len(signal))])
signal_avg_dev = signal_exp - signal_avg

COLORS = {
    'red': '#dc322f',
    'orange': '#cb4b16',
    'yellow': '#b58900',
    'green': '#859900',
    'blue': '#268bd2',
    'violet': '#6c71c4',
    'magenta': '#d33682',
    'cyan': '#2aa198',
    'black': '#002b36',
    'gray': '#839496',
    'dark_gray': '#073642'
}

legend = {
    'sta0000': data[1][6],
    'sta0001': data[2][6],
    'sta0002': data[3][6],
    'sta0003': data[4][6],
    'sta0004': data[5][6],
    'sta0005': data[6][6],
    'sta0006': data[7][6]
}

plt.rc('font', family='Liberation Serif')
plt.style.use('dark_background')
fig = plt.figure(figsize=(8, 8), dpi=100)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(atten[:, 0], signal_exp, color=COLORS['gray'], alpha=1.0, label='Expected')
if CHANNEL == 6:
    ax.plot(atten[:, 0], signal[:, 0], color=COLORS['red'], alpha=1.0, label=legend['sta0000']) # TODO: Make generic
if CHANNEL == 36:
    ax.plot(atten[:, 1], signal[:, 1], color=COLORS['orange'], alpha=1.0, label=legend['sta0001']) # TODO: Make generic
ax.plot(atten[:, 2], signal[:, 2], color=COLORS['yellow'], alpha=1.0, label=legend['sta0002'])
ax.plot(atten[:, 3], signal[:, 3], color=COLORS['green'],  alpha=1.0, label=legend['sta0003'])
ax.plot(atten[:, 4], signal[:, 4], color=COLORS['cyan'],   alpha=1.0, label=legend['sta0004'])
ax.plot(atten[:, 5], signal[:, 5], color=COLORS['blue'],   alpha=1.0, label=legend['sta0005'])
ax.plot(atten[:, 6], signal[:, 6], color=COLORS['violet'], alpha=1.0, label=legend['sta0006'])
ax.set_title('Attenuation vs. Signal:\n'
             + F'SSID={data[7][14]}, '
             + F'Channel={CHANNEL}, '
             + F'Bandwidth={BANDWIDTH}, '
             + F'Antenna={ANTENNA_LEGEND[ANTENNA]}')
ax.set_xlabel('Attenuation (dB)')
ax.set_ylabel('RSSI (dBm)')
ax.set_yticks(range(-30, -110, -5))
ax.set_xticks(range(20, 100, 5))
plt.grid(color=COLORS['dark_gray'], linestyle='-', linewidth=1)
plt.legend()
plt.savefig(F'{PNG_OUTPUT_DIR}/{CHANNEL}_{ANTENNA}_{BANDWIDTH}_signal_atten.png')

plt.style.use('dark_background')
fig = plt.figure(figsize=(8, 8), dpi=100)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
if CHANNEL == 6:
    ax.plot(atten[:, 0], signal_dev[:, 0], color=COLORS['red'], label=legend['sta0000'])
if CHANNEL == 36:
    ax.plot(atten[:, 1], signal_dev[:, 1], color=COLORS['orange'],  label=legend['sta0001'])
ax.plot(atten[:, 2], signal_dev[:, 2], color=COLORS['yellow'], label=legend['sta0002'])
ax.plot(atten[:, 2], signal_dev[:, 3], color=COLORS['green'], label=legend['sta0003'])
ax.plot(atten[:, 2], signal_dev[:, 4], color=COLORS['cyan'], label=legend['sta0004'])
ax.plot(atten[:, 2], signal_dev[:, 5], color=COLORS['blue'], label=legend['sta0005'])
ax.plot(atten[:, 2], signal_dev[:, 6], color=COLORS['violet'], label=legend['sta0006'])
ax.set_title('Atteunuation vs. Signal Deviation:\n'
             + F'SSID={data[7][14]}, '
             + F'Channel={CHANNEL}, '
             + F'Bandwidth={BANDWIDTH}, '
             + F'Antenna={ANTENNA_LEGEND[ANTENNA]}')
ax.set_xlabel('Attenuation (dB)')
ax.set_ylabel('RSSI (dBm)')
ax.set_yticks(range(-5, 30, 5))
ax.set_xticks(range(20, 100, 5))
plt.grid(color=COLORS['dark_gray'], linestyle='-', linewidth=1)
plt.legend()
plt.savefig(F'{PNG_OUTPUT_DIR}/{CHANNEL}_{ANTENNA}_{BANDWIDTH}_signal_deviation_atten.png')

check_data(signal, signal_exp)
sys.exit(0)
