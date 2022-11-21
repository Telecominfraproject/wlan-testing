#!/usr/bin/env python3
import importlib
from time import sleep
# import pandas as pd
import sys
import os
from pprint import pformat
import logging
import traceback

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase

logger = logging.getLogger(__name__)

# Probe data can change frequently. It is recommended to update


class ProbePort(LFCliBase):
    def __init__(self,
                 lfhost=None,
                 lfport='8080',
                 debug=False,
                 eid_str=None):
        super().__init__(_lfjson_host=lfhost,
                         _lfjson_port=lfport,
                         _debug=debug)
        hunks = eid_str.split(".")
        self.eid_str = eid_str
        self.probepath = "/probe/1/%s/%s" % (hunks[-2], hunks[-1])
        self.response = None
        self.signals = None
        self.ofdma = False

        self.tx_bitrate = None
        self.tx_mcs = None
        self.tx_nss = None
        self.tx_mbit = None
        self.tx_mhz = None
        self.tx_gi = None
        self.tx_duration = None
        self.tx_mbit_calc = None
        self.tx_data_rate_gi_short_Mbps = None
        self.tx_data_rate_gi_long_Mbps = None

        self.rx_bitrate = None
        self.rx_mcs = None
        self.rx_nss = None
        self.rx_mbit = None
        self.rx_mhz = None
        self.rx_gi = None
        self.rx_duration = None
        self.rx_mbit_calc = None
        self.rx_data_rate_gi_short_Mbps = None
        self.rx_data_rate_gi_long_Mbps = None

        self.data_rate = None
        # folder = os.path.dirname(__file__)

    def refreshProbe(self):
        self.json_post(self.probepath, {})
        sleep(0.2)
        response = self.json_get(self.probepath)
        self.response = response
        if self.debug:
            logger.debug("probepath (eid): {probepath}".format(probepath=self.probepath))
            logger.debug(pformat("Probe response: {response}".format(response=self.response)))
        text = self.response['probe-results'][0][self.eid_str]['probe results'].split('\n')
        signals = [x.strip('\t').split('\t') for x in text if 'signal' in x]
        keys = [x[0].strip(' ').strip(':') for x in signals]
        values = [x[1].strip('dBm').strip(' ') for x in signals]
        if self.debug:
            logger.debug("signals keys: {keys}".format(keys=keys))
            logger.debug("signals values: {values}".format(values=values))
        self.signals = dict(zip(keys, values))

        try:
            tx_bitrate = [x for x in text if 'tx bitrate' in x][0].replace('\t', ' ')
            # if 'HE' in tx_bitrate:
            #    logger.info("HE not supported ")
            logger.debug("tx_bitrate {tx_bitrate}".format(tx_bitrate=tx_bitrate))
            self.tx_bitrate = tx_bitrate.split(':')[-1].strip(' ')
            if 'MHz' in tx_bitrate:
                self.tx_mhz = [x.strip('\t') for x in text if 'tx bitrate' in x][0].split('MHz')[0].rsplit(' ')[-1].strip(
                    ' ')
                logger.debug("tx_mhz {tx_mhz}".format(tx_mhz=self.tx_mhz))
            else:
                self.tx_mhz = 20
                logger.debug("HT: tx_mhz {tx_mhz}".format(tx_mhz=self.tx_mhz))
            tx_mcs = [x.strip('\t') for x in text if 'tx bitrate' in x][0].split(':')[1].strip('\t')
            if 'MCS' in tx_mcs:
                self.tx_mcs = int(tx_mcs.split('MCS')[1].strip(' ').split(' ')[0])
                logger.debug("self.tx_mcs {tx_mcs}".format(tx_mcs=self.tx_mcs))
                if 'NSS' in text:
                    self.tx_nss = [x.strip('\t') for x in text if 'tx bitrate' in x][0].split('NSS')[1].strip(' ')
                else:
                    # nss is not present need to derive from MCS for HT
                    if 0 <= self.tx_mcs <= 7:
                        self.tx_nss = 1
                    elif 8 <= self.tx_mcs <= 15:
                        self.tx_nss = 2
                    elif 16 <= self.tx_mcs <= 23:
                        self.tx_nss = 3
                    elif 24 <= self.tx_mcs <= 31:
                        self.tx_nss = 4
                logger.debug("tx_nss {tx_nss}".format(tx_nss=self.tx_nss))
                self.tx_mbit = float(self.tx_bitrate.split(' ')[0])
                logger.debug("tx_mbit {tx_mbit}".format(tx_mbit=self.tx_mbit))
                if 'HE' in tx_bitrate:
                    self.calculated_data_rate_tx_HE()
                elif 'VHT' in tx_bitrate:
                    self.calculated_data_rate_tx_VHT()
                else:
                    self.calculated_data_rate_tx_HT()
            else:
                logger.debug("No tx MCS value:{tx_bitrate}".format(tx_bitrate=tx_bitrate))

            rx_bitrate = [x for x in text if 'rx bitrate' in x][0].replace('\t', ' ')
            logger.debug("rx_bitrate {rx_bitrate}".format(rx_bitrate=rx_bitrate))
            self.rx_bitrate = rx_bitrate.split(':')[-1].strip(' ')
            logger.debug("self.rx_bitrate {rx_bitrate}".format(rx_bitrate=self.rx_bitrate))
            # rx will received : 6Mbps encoding is legacy frame
            # for 24g - MHz is 20
            # try:
            if 'MHz' in rx_bitrate:
                self.rx_mhz = [x.strip('\t') for x in text if 'rx bitrate' in x][0].split('MHz')[0].rsplit(' ')[
                    -1].strip(' ')
                logger.debug("rx_mhz {rx_mhz}".format(rx_mhz=self.rx_mhz))
            else:
                self.rx_mhz = 20

            rx_mcs = [x.strip('\t') for x in text if 'rx bitrate' in x][0].split(':')[1].strip('\t')
            # MCS is not in the 6.0MBit/s frame
            if 'MCS' in rx_mcs:
                self.rx_mcs = int(rx_mcs.split('MCS')[1].strip(' ').split(' ')[0])
                logger.debug("self.rx_mcs {rx_mcs}".format(rx_mcs=self.rx_mcs))
                if 'NSS' in text:
                    self.rx_nss = [x.strip('\t') for x in text if 'rx bitrate' in x][0].split('NSS')[1].strip(' ')
                else:
                    # nss is not present need to derive from MCS for HT
                    if 0 <= self.rx_mcs <= 7:
                        self.rx_nss = 1
                    elif 8 <= self.rx_mcs <= 15:
                        self.rx_nss = 2
                    elif 16 <= self.rx_mcs <= 23:
                        self.rx_nss = 3
                    elif 24 <= self.rx_mcs <= 31:
                        self.rx_nss = 4

                self.rx_mbit = self.rx_bitrate.split(' ')[0]
                logger.debug("rx_nss {rx_nss}".format(rx_nss=self.rx_nss))
                self.rx_mbit = float(self.rx_bitrate.split(' ')[0])
                logger.debug("rx_mbit {rx_mbit}".format(rx_mbit=self.rx_mbit))
                if 'HE' in rx_bitrate:
                    self.calculated_data_rate_rx_HE()
                elif 'VHT' in rx_bitrate:
                    self.calculated_data_rate_rx_VHT()
                else:
                    self.calculated_data_rate_rx_HT()
            else:
                logger.debug("No rx MCS value:{rx_bitrate}".format(rx_bitrate=rx_bitrate))
            return True
        except Exception as x:
            logger.warning("Probe response list was empty.")
            traceback.print_exception(Exception, x, x.__traceback__, chain=True)
            return False

    def getSignalAvgCombined(self):
        return self.signals['signal avg'].split(' ')[0]

    def getSignalAvgPerChain(self):
        return ' '.join(self.signals['signal avg'].split(' ')[1:])

    def getSignalCombined(self):
        return self.signals['signal'].split(' ')[0]

    def getSignalPerChain(self):
        return ' '.join(self.signals['signal'].split(' ')[1:])

    def getBeaconSignalAvg(self):
        return ' '.join(self.signals['beacon signal avg']).replace(' ', '')

    def calculated_data_rate_tx_HT(self):
        logger.info("calculated_data_rate_tx_HT")
        # TODO compare with standard for 40 MHz if values change
        N_sd = 0  # Number of Data Subcarriers based on modulation and bandwith
        N_bpscs = 0  # Number of coded bits per Subcarrier(Determined by the modulation, MCS)
        R = 0  # coding ,  (Determined by the modulation, MCS )
        N_ss = 0  # Number of Spatial Streams
        T_dft = 3.2 * 10 ** -6  # Constant for HT
        T_gi_short = .4 * 10 ** -6  # Guard index.
        T_gi_long = .8 * 10 ** -6  # Guard index.
        bw = 20
        # Note the T_gi is not exactly know so need to calculate bothh with .4 and .8
        # the nubmer of Data Subcarriers is based on modulation and bandwith
        bw = int(self.tx_mhz)
        logger.info("Mhz {Mhz}".format(Mhz=self.tx_mhz))
        if bw == 20:
            N_sd = 52
        elif bw == 40:
            N_sd = 108
        elif bw == 80:
            N_sd = 234
        elif bw == 160:
            N_sd = 468
        else:
            logger.info("For HT if cannot be read bw is assumed to be 20")
            N_sd = 52
            self.tx_mhz = 20

        # NSS
        N_ss = self.tx_nss
        # MCS (Modulation Coding Scheme) determines the constands
        # MCS 0 == Modulation BPSK R = 1/2 ,  N_bpscs = 1,
        # Only for HT configuration
        if self.tx_mcs == 0 or self.tx_mcs == 8 or self.tx_mcs == 16 or self.tx_mcs == 24:
            R = 1 / 2
            N_bpscs = 1
        # MCS 1 == Modulation QPSK R = 1/2 , N_bpscs = 2
        elif self.tx_mcs == 1 or self.tx_mcs == 9 or self.tx_mcs == 17 or self.tx_mcs == 25:
            R = 1 / 2
            N_bpscs = 2
        # MCS 2 == Modulation QPSK R = 3/4 , N_bpscs = 2
        elif self.tx_mcs == 2 or self.tx_mcs == 10 or self.tx_mcs == 18 or self.tx_mcs == 26:
            R = 3 / 4
            N_bpscs = 2
        # MCS 3 == Modulation 16-QAM R = 1/2 , N_bpscs = 4
        elif self.tx_mcs == 3 or self.tx_mcs == 11 or self.tx_mcs == 19 or self.tx_mcs == 27:
            R = 1 / 2
            N_bpscs = 4
        # MCS 4 == Modulation 16-QAM R = 3/4 , N_bpscs = 4
        elif self.tx_mcs == 4 or self.tx_mcs == 12 or self.tx_mcs == 20 or self.tx_mcs == 28:
            R = 3 / 4
            N_bpscs = 4
        # MCS 5 == Modulation 64-QAM R = 2/3 , N_bpscs = 6
        elif self.tx_mcs == 5 or self.tx_mcs == 13 or self.tx_mcs == 21 or self.tx_mcs == 29:
            R = 2 / 3
            N_bpscs = 6
        # MCS 6 == Modulation 64-QAM R = 3/4 , N_bpscs = 6
        elif self.tx_mcs == 6 or self.tx_mcs == 14 or self.tx_mcs == 22 or self.tx_mcs == 30:
            R = 3 / 4
            N_bpscs = 6
        # MCS 7 == Modulation 64-QAM R = 5/6 , N_bpscs = 6
        elif self.tx_mcs == 7 or self.tx_mcs == 15 or self.tx_mcs == 23 or self.tx_mcs == 31:
            R = 5 / 6
            N_bpscs = 6

        logger.debug(
            "tx: mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_short {T_gi_short}".format(
                mcs=self.tx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_short=T_gi_short))

        self.tx_data_rate_gi_short_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_short)) / 1000000
        logger.debug("tx_data_rate gi_short {data_rate} Mbit/s".format(data_rate=self.tx_data_rate_gi_short_Mbps))

        logger.debug(
            "tx: mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_long {T_gi_long}".format(
                mcs=self.tx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_long=T_gi_long))

        self.tx_data_rate_gi_long_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_long)) / 1000000
        logger.info("data_rate gi_long {data_rate} Mbps".format(data_rate=self.tx_data_rate_gi_long_Mbps))

        if abs(self.tx_mbit - self.tx_data_rate_gi_short_Mbps) <= abs(self.tx_mbit - self.tx_data_rate_gi_long_Mbps):
            self.tx_mbit_calc = self.tx_data_rate_gi_short_Mbps
            self.tx_gi = T_gi_short
        else:
            self.tx_mbit_calc = self.tx_data_rate_gi_long_Mbps
            self.tx_gi = T_gi_long

    def calculated_data_rate_rx_HT(self):
        logger.info("calculated_data_rate_rx_HT")
        N_sd = 0  # Number of Data Subcarriers based on modulation and bandwith
        N_bpscs = 0  # Number of coded bits per Subcarrier(Determined by the modulation, MCS)
        R = 0  # coding ,  (Determined by the modulation, MCS )
        N_ss = 0  # Number of Spatial Streams
        T_dft = 3.2 * 10 ** -6  # Constant for HT
        T_gi_short = .4 * 10 ** -6  # Guard index.
        T_gi_long = .8 * 10 ** -6  # Guard index.
        bw = 20
        # Note the T_gi is not exactly know so need to calculate bothh with .4 and .8
        # the nubmer of Data Subcarriers is based on modulation and bandwith

        bw = int(self.rx_mhz)
        logger.info("Mhz {Mhz}".format(Mhz=self.rx_mhz))
        if bw == 20:
            N_sd = 52
        elif bw == 40:
            N_sd = 108
        elif bw == 80:
            N_sd = 234
        elif bw == 160:
            N_sd = 468
        else:
            logger.info("For HT if cannot be read bw is assumed to be 20")
            N_sd = 52
            self.rx_mhz = 20
        # NSS
        N_ss = self.rx_nss
        # MCS (Modulation Coding Scheme) determines the constands
        # MCS 0 == Modulation BPSK R = 1/2 ,  N_bpscs = 1,
        # Only for HT configuration
        if self.rx_mcs == 0 or self.rx_mcs == 8 or self.rx_mcs == 16 or self.rx_mcs == 24:
            R = 1 / 2
            N_bpscs = 1
        # MCS 1 == Modulation QPSK R = 1/2 , N_bpscs = 2
        elif self.rx_mcs == 1 or self.rx_mcs == 9 or self.rx_mcs == 17 or self.rx_mcs == 25:
            R = 1 / 2
            N_bpscs = 2
        # MCS 2 == Modulation QPSK R = 3/4 , N_bpscs = 2
        elif self.rx_mcs == 2 or self.rx_mcs == 10 or self.rx_mcs == 18 or self.rx_mcs == 26:
            R = 3 / 4
            N_bpscs = 2
        # MCS 3 == Modulation 16-QAM R = 1/2 , N_bpscs = 4
        elif self.rx_mcs == 3 or self.rx_mcs == 11 or self.rx_mcs == 19 or self.rx_mcs == 27:
            R = 1 / 2
            N_bpscs = 4
        # MCS 4 == Modulation 16-QAM R = 3/4 , N_bpscs = 4
        elif self.rx_mcs == 4 or self.rx_mcs == 12 or self.rx_mcs == 20 or self.rx_mcs == 28:
            R = 3 / 4
            N_bpscs = 4
        # MCS 5 == Modulation 64-QAM R = 2/3 , N_bpscs = 6
        elif self.rx_mcs == 5 or self.rx_mcs == 13 or self.rx_mcs == 21 or self.rx_mcs == 29:
            R = 2 / 3
            N_bpscs = 6
        # MCS 6 == Modulation 64-QAM R = 3/4 , N_bpscs = 6
        elif self.rx_mcs == 6 or self.rx_mcs == 14 or self.rx_mcs == 22 or self.rx_mcs == 30:
            R = 3 / 4
            N_bpscs = 6
        # MCS 7 == Modulation 64-QAM R = 5/6 , N_bpscs = 6
        elif self.rx_mcs == 7 or self.rx_mcs == 15 or self.rx_mcs == 23 or self.rx_mcs == 31:
            R = 5 / 6
            N_bpscs = 6
        logger.debug(
            "mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_short {T_gi_short}".format(
                mcs=self.rx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_short=T_gi_short))
        self.rx_data_rate_gi_short_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_short)) / 1000000
        logger.debug("rx_data_rate gi_short {data_rate} Mbit/s".format(data_rate=self.rx_data_rate_gi_short_Mbps))
        logger.debug(
            "mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_long {T_gi_long}".format(
                mcs=self.rx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_long=T_gi_long))
        self.rx_data_rate_gi_long_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_long)) / 1000000
        logger.debug("rx_data_rate gi_long {data_rate} Mbps".format(data_rate=self.rx_data_rate_gi_long_Mbps))
        if abs(self.rx_mbit - self.rx_data_rate_gi_short_Mbps) <= abs(
                self.rx_mbit - self.rx_data_rate_gi_long_Mbps):
            self.rx_mbit_calc = self.rx_data_rate_gi_short_Mbps
            self.rx_gi = T_gi_short
        else:
            self.rx_mbit_calc = self.rx_data_rate_gi_long_Mbps
            self.rx_gi = T_gi_long

    def calculated_data_rate_tx_VHT(self):
        logger.info("calculated_data_rate_tx_VHT")
        # TODO compare with standard for 40 MHz if values change
        N_sd = 0  # Number of Data Subcarriers based on modulation and bandwith
        N_bpscs = 0  # Number of coded bits per Subcarrier(Determined by the modulation, MCS)
        R = 0  # coding ,  (Determined by the modulation, MCS )
        N_ss = 0  # Number of Spatial Streams
        T_dft = 3.2 * 10 ** -6  # Constant for HT
        T_gi_short = .4 * 10 ** -6  # Guard index.
        T_gi_long = .8 * 10 ** -6  # Guard index.
        bw = 20
        # Note the T_gi is not exactly know so need to calculate bothh with .4 and .8
        # the nubmer of Data Subcarriers is based on modulation and bandwith
        bw = int(self.tx_mhz)

        logger.info("Mhz {Mhz}".format(Mhz=self.tx_mhz))
        if bw == 20:
            N_sd = 52
        elif bw == 40:
            N_sd = 108
        elif bw == 80:
            N_sd = 234
        elif bw == 160:
            N_sd = 468
        else:
            logger.info("For HT if cannot be read bw is assumed to be 20")
            N_sd = 52
            self.tx_mhz = 20

        # NSS
        N_ss = self.tx_nss
        # MCS (Modulation Coding Scheme) determines the constands
        # MCS 0 == Modulation BPSK R = 1/2 ,  N_bpscs = 1,
        # Only for HT configuration
        if self.tx_mcs == 0:
            R = 1 / 2
            N_bpscs = 1
        # MCS 1 == Modulation QPSK R = 1/2 , N_bpscs = 2
        elif self.tx_mcs == 1:
            R = 1 / 2
            N_bpscs = 2
        # MCS 2 == Modulation QPSK R = 3/4 , N_bpscs = 2
        elif self.tx_mcs == 2:
            R = 3 / 4
            N_bpscs = 2
        # MCS 3 == Modulation 16-QAM R = 1/2 , N_bpscs = 4
        elif self.tx_mcs == 3:
            R = 1 / 2
            N_bpscs = 4
        # MCS 4 == Modulation 16-QAM R = 3/4 , N_bpscs = 4
        elif self.tx_mcs == 4:
            R = 3 / 4
            N_bpscs = 4
        # MCS 5 == Modulation 64-QAM R = 2/3 , N_bpscs = 6
        elif self.tx_mcs == 5:
            R = 2 / 3
            N_bpscs = 6
        # MCS 6 == Modulation 64-QAM R = 3/4 , N_bpscs = 6
        elif self.tx_mcs == 6:
            R = 3 / 4
            N_bpscs = 6
        # MCS 7 == Modulation 64-QAM R = 5/6 , N_bpscs = 6
        elif self.tx_mcs == 7:
            R = 5 / 6
            N_bpscs = 6
        # MCS 8 == Modulation 256-QAM R = 3/4 , N_bpscs = 8
        elif self.tx_mcs == 8:
            R = 3 / 4
            N_bpscs = 8
        # MCS 9 == Modulation 256-QAM R = 5/6 , N_bpscs = 8
        elif self.tx_mcs == 9:
            R = 5 / 6
            N_bpscs = 8

        logger.debug(
            "tx: mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_short {T_gi_short}".format(
                mcs=self.tx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_short=T_gi_short))

        self.tx_data_rate_gi_short_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_short)) / 1000000
        logger.debug("tx_data_rate gi_short {data_rate} Mbit/s".format(data_rate=self.tx_data_rate_gi_short_Mbps))

        logger.debug(
            "tx: mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_long {T_gi_long}".format(
                mcs=self.tx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_long=T_gi_long))

        self.tx_data_rate_gi_long_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_long)) / 1000000
        logger.debug("data_rate gi_long {data_rate} Mbps".format(data_rate=self.tx_data_rate_gi_long_Mbps))

        if abs(self.tx_mbit - self.tx_data_rate_gi_short_Mbps) <= abs(self.tx_mbit - self.tx_data_rate_gi_long_Mbps):
            self.tx_mbit_calc = self.tx_data_rate_gi_short_Mbps
            self.tx_gi = T_gi_short
        else:
            self.tx_mbit_calc = self.tx_data_rate_gi_long_Mbps
            self.tx_gi = T_gi_long

    def calculated_data_rate_rx_VHT(self):
        logger.info("calculated_data_rate_rx_VHT")
        N_sd = 0  # Number of Data Subcarriers based on modulation and bandwith
        N_bpscs = 0  # Number of coded bits per Subcarrier(Determined by the modulation, MCS)
        R = 0  # coding ,  (Determined by the modulation, MCS )
        N_ss = 0  # Number of Spatial Streams
        T_dft = 3.2 * 10 ** -6  # Constant for HT
        T_gi_short = .4 * 10 ** -6  # Guard index.
        T_gi_long = .8 * 10 ** -6  # Guard index.
        # Note the T_gi is not exactly know so need to calculate bothh with .4 and .8
        # the nubmer of Data Subcarriers is based on modulation and bandwith
        bw = int(self.rx_mhz)
        logger.info("Mhz {Mhz}".format(Mhz=self.rx_mhz))
        if bw == 20:
            N_sd = 52
        elif bw == 40:
            N_sd = 108
        elif bw == 80:
            N_sd = 234
        elif bw == 160:
            N_sd = 468
        else:
            logger.info("For HT if cannot be read bw is assumed to be 20")
            N_sd = 52
            self.rx_mhz = 20
        # NSS
        N_ss = self.rx_nss
        # MCS (Modulation Coding Scheme) determines the constands
        # MCS 0 == Modulation BPSK R = 1/2 ,  N_bpscs = 1,
        # Only for HT configuration
        if self.rx_mcs == 0:
            R = 1 / 2
            N_bpscs = 1
        # MCS 1 == Modulation QPSK R = 1/2 , N_bpscs = 2
        elif self.rx_mcs == 1:
            R = 1 / 2
            N_bpscs = 2
        # MCS 2 == Modulation QPSK R = 3/4 , N_bpscs = 2
        elif self.rx_mcs == 2:
            R = 3 / 4
            N_bpscs = 2
        # MCS 3 == Modulation 16-QAM R = 1/2 , N_bpscs = 4
        elif self.rx_mcs == 3:
            R = 1 / 2
            N_bpscs = 4
        # MCS 4 == Modulation 16-QAM R = 3/4 , N_bpscs = 4
        elif self.rx_mcs == 4:
            R = 3 / 4
            N_bpscs = 4
        # MCS 5 == Modulation 64-QAM R = 2/3 , N_bpscs = 6
        elif self.rx_mcs == 5:
            R = 2 / 3
            N_bpscs = 6
        # MCS 6 == Modulation 64-QAM R = 3/4 , N_bpscs = 6
        elif self.rx_mcs == 6:
            R = 3 / 4
            N_bpscs = 6
        # MCS 7 == Modulation 64-QAM R = 5/6 , N_bpscs = 6
        elif self.rx_mcs == 7:
            R = 5 / 6
            N_bpscs = 6
        # MCS 8 == Modulation 256-QAM R = 3/4 , N_bpscs = 8
        elif self.rx_mcs == 8:
            R = 3 / 4
            N_bpscs = 8
        # MCS 9 == Modulation 256-QAM R = 5/6 , N_bpscs = 8
        elif self.rx_mcs == 9:
            R = 5 / 6
            N_bpscs = 8
        logger.debug(
            "mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_short {T_gi_short}".format(
                mcs=self.rx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_short=T_gi_short))
        self.rx_data_rate_gi_short_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_short)) / 1000000
        logger.debug("rx_data_rate gi_short {data_rate} Mbit/s".format(data_rate=self.rx_data_rate_gi_short_Mbps))
        logger.debug(
            "mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_long {T_gi_long}".format(
                mcs=self.rx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_long=T_gi_long))
        self.rx_data_rate_gi_long_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_long)) / 1000000
        logger.debug("rx_data_rate gi_long {data_rate} Mbps".format(data_rate=self.rx_data_rate_gi_long_Mbps))
        if abs(self.rx_mbit - self.rx_data_rate_gi_short_Mbps) <= abs(
                self.rx_mbit - self.rx_data_rate_gi_long_Mbps):
            self.rx_mbit_calc = self.rx_data_rate_gi_short_Mbps
            self.rx_gi = T_gi_short
        else:
            self.rx_mbit_calc = self.rx_data_rate_gi_long_Mbps
            self.rx_gi = T_gi_long
        ##########################################
        #
        # HE no OFDMA - changes the calculations
        #
        ###########################################

    def calculated_data_rate_tx_HE(self):
        logger.info("calculated_data_rate_tx_HE")
        # TODO compare with standard for 40 MHz if values change
        N_sd = 0  # Number of Data Subcarriers based on modulation and bandwith
        N_bpscs = 0  # Number of coded bits per Subcarrier(Determined by the modulation, MCS)
        R = 0  # coding ,  (Determined by the modulation, MCS )
        N_ss = 0  # Number of Spatial Streams
        T_dft = 3.2 * 10 ** -6  # Constant for HT
        T_gi_short = .4 * 10 ** -6  # Guard index.
        T_gi_long = .8 * 10 ** -6  # Guard index.
        bw = 20
        # Note the T_gi is not exactly know so need to calculate bothh with .4 and .8
        # the nubmer of Data Subcarriers is based on modulation and bandwith
        bw = int(self.tx_mhz)
        logger.info("Mhz {Mhz}".format(Mhz=self.tx_mhz))
        if bw == 20:
            N_sd = 52
        elif bw == 40:
            N_sd = 108
        elif bw == 80:
            N_sd = 234
        elif bw == 160:
            N_sd = 468
        else:
            logger.info("For HT if cannot be read bw is assumed to be 20")
            N_sd = 52
            self.tx_mhz = 20

        # NSS
        N_ss = self.tx_nss
        # MCS (Modulation Coding Scheme) determines the constands
        # MCS 0 == Modulation BPSK R = 1/2 ,  N_bpscs = 1,
        # Only for HT configuration
        if self.tx_mcs == 0:
            R = 1 / 2
            N_bpscs = 1
        # MCS 1 == Modulation QPSK R = 1/2 , N_bpscs = 2
        elif self.tx_mcs == 1:
            R = 1 / 2
            N_bpscs = 2
        # MCS 2 == Modulation QPSK R = 3/4 , N_bpscs = 2
        elif self.tx_mcs == 2:
            R = 3 / 4
            N_bpscs = 2
        # MCS 3 == Modulation 16-QAM R = 1/2 , N_bpscs = 4
        elif self.tx_mcs == 3:
            R = 1 / 2
            N_bpscs = 4
        # MCS 4 == Modulation 16-QAM R = 3/4 , N_bpscs = 4
        elif self.tx_mcs == 4:
            R = 3 / 4
            N_bpscs = 4
        # MCS 5 == Modulation 64-QAM R = 2/3 , N_bpscs = 6
        elif self.tx_mcs == 5:
            R = 2 / 3
            N_bpscs = 6
        # MCS 6 == Modulation 64-QAM R = 3/4 , N_bpscs = 6
        elif self.tx_mcs == 6:
            R = 3 / 4
            N_bpscs = 6
        # MCS 7 == Modulation 64-QAM R = 5/6 , N_bpscs = 6
        elif self.tx_mcs == 7:
            R = 5 / 6
            N_bpscs = 6
        # MCS 8 == Modulation 256-QAM R = 3/4 , N_bpscs = 8
        elif self.tx_mcs == 8:
            R = 3 / 4
            N_bpscs = 8
        # MCS 9 == Modulation 256-QAM R = 5/6 , N_bpscs = 8
        elif self.tx_mcs == 9:
            R = 5 / 6
            N_bpscs = 8

        logger.debug(
            "tx: mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_short {T_gi_short}".format(
                mcs=self.tx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_short=T_gi_short))

        self.tx_data_rate_gi_short_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_short)) / 1000000
        logger.debug("tx_data_rate gi_short {data_rate} Mbit/s".format(data_rate=self.tx_data_rate_gi_short_Mbps))

        logger.debug(
            "tx: mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_long {T_gi_long}".format(
                mcs=self.tx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_long=T_gi_long))

        self.tx_data_rate_gi_long_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_long)) / 1000000
        logger.debug("data_rate gi_long {data_rate} Mbps".format(data_rate=self.tx_data_rate_gi_long_Mbps))

        if abs(self.tx_mbit - self.tx_data_rate_gi_short_Mbps) <= abs(self.tx_mbit - self.tx_data_rate_gi_long_Mbps):
            self.tx_mbit_calc = self.tx_data_rate_gi_short_Mbps
            self.tx_gi = T_gi_short
        else:
            self.tx_mbit_calc = self.tx_data_rate_gi_long_Mbps
            self.tx_gi = T_gi_long

    def calculated_data_rate_rx_HE(self):
        logger.info("calculated_data_rate_rx_HE")
        N_sd = 0  # Number of Data Subcarriers based on modulation and bandwith
        N_bpscs = 0  # Number of coded bits per Subcarrier(Determined by the modulation, MCS)
        R = 0  # coding ,  (Determined by the modulation, MCS )
        N_ss = 0  # Number of Spatial Streams
        T_dft = 3.2 * 10 ** -6  # Constant for HT
        T_gi_short = .4 * 10 ** -6  # Guard index.
        T_gi_long = .8 * 10 ** -6  # Guard index.
        # Note the T_gi is not exactly know so need to calculate bothh with .4 and .8
        # the nubmer of Data Subcarriers is based on modulation and bandwith
        bw = int(self.rx_mhz)
        logger.info("Mhz {Mhz}".format(Mhz=self.rx_mhz))
        if bw == 20:
            N_sd = 52
        elif bw == 40:
            N_sd = 108
        elif bw == 80:
            N_sd = 234
        elif bw == 160:
            N_sd = 468
        else:
            logger.info("For HT if cannot be read bw is assumed to be 20")
            N_sd = 52
            self.rx_mhz = 20
        # NSS
        N_ss = self.rx_nss
        # MCS (Modulation Coding Scheme) determines the constands
        # MCS 0 == Modulation BPSK R = 1/2 ,  N_bpscs = 1,
        # Only for HT configuration
        if self.rx_mcs == 0:
            R = 1 / 2
            N_bpscs = 1
        # MCS 1 == Modulation QPSK R = 1/2 , N_bpscs = 2
        elif self.rx_mcs == 1:
            R = 1 / 2
            N_bpscs = 2
        # MCS 2 == Modulation QPSK R = 3/4 , N_bpscs = 2
        elif self.rx_mcs == 2:
            R = 3 / 4
            N_bpscs = 2
        # MCS 3 == Modulation 16-QAM R = 1/2 , N_bpscs = 4
        elif self.rx_mcs == 3:
            R = 1 / 2
            N_bpscs = 4
        # MCS 4 == Modulation 16-QAM R = 3/4 , N_bpscs = 4
        elif self.rx_mcs == 4:
            R = 3 / 4
            N_bpscs = 4
        # MCS 5 == Modulation 64-QAM R = 2/3 , N_bpscs = 6
        elif self.rx_mcs == 5:
            R = 2 / 3
            N_bpscs = 6
        # MCS 6 == Modulation 64-QAM R = 3/4 , N_bpscs = 6
        elif self.rx_mcs == 6:
            R = 3 / 4
            N_bpscs = 6
        # MCS 7 == Modulation 64-QAM R = 5/6 , N_bpscs = 6
        elif self.rx_mcs == 7:
            R = 5 / 6
            N_bpscs = 6
        # MCS 8 == Modulation 256-QAM R = 3/4 , N_bpscs = 8
        elif self.rx_mcs == 8:
            R = 3 / 4
            N_bpscs = 8
        # MCS 9 == Modulation 256-QAM R = 5/6 , N_bpscs = 8
        elif self.rx_mcs == 9:
            R = 5 / 6
            N_bpscs = 8
        logger.debug(
            "mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_short {T_gi_short}".format(
                mcs=self.rx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_short=T_gi_short))
        self.rx_data_rate_gi_short_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_short)) / 1000000
        logger.debug("rx_data_rate gi_short {data_rate} Mbit/s".format(data_rate=self.rx_data_rate_gi_short_Mbps))
        logger.debug(
            "mcs {mcs} N_sd {N_sd} N_bpscs {N_bpscs} R {R} N_ss {N_ss}  T_dft {T_dft} T_gi_long {T_gi_long}".format(
                mcs=self.rx_mcs, N_sd=N_sd, N_bpscs=N_bpscs, R=R, N_ss=N_ss, T_dft=T_dft, T_gi_long=T_gi_long))
        self.rx_data_rate_gi_long_Mbps = ((N_sd * N_bpscs * R * float(N_ss)) / (T_dft + T_gi_long)) / 1000000
        logger.debug("rx_data_rate gi_long {data_rate} Mbps".format(data_rate=self.rx_data_rate_gi_long_Mbps))
        if abs(self.rx_mbit - self.rx_data_rate_gi_short_Mbps) <= abs(
                self.rx_mbit - self.rx_data_rate_gi_long_Mbps):
            self.rx_mbit_calc = self.rx_data_rate_gi_short_Mbps
            self.rx_gi = T_gi_short
        else:
            self.rx_mbit_calc = self.rx_data_rate_gi_long_Mbps
            self.rx_gi = T_gi_long
