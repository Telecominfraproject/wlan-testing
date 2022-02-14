#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Not auto-generated
##################################################

from gnuradio import blocks
#from gnuradio import eng_notation
from gnuradio import gr
#from gnuradio.eng_option import eng_option
#from gnuradio.filter import firdes
#from optparse import OptionParser
import osmosdr
import time
import getopt, sys
import os
import signal

default_gain = 14
default_if_gain = 27
default_bb_gain = 20
gain = default_if_gain
if_gain = default_if_gain
bb_gain = default_bb_gain
freq = 5300000000
vector = []
pid_file = "lf_hackrf_py.pid"
mgt_pipe = -1
sample_mod = 2
repeat_onoff = True

class top_block(gr.top_block):

    def __init__(self):
        global freq
        global vector
        global sample_mod
        global repeat_onoff
        global gain
        global if_gain
        global bb_gain

        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        #self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" ) # this is mysterious
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=1 " )
        self.osmosdr_sink_0.set_sample_rate(1e6 * sample_mod)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(20e6, 0)

        #print vector
        self.blocks_vector_source_x_0 = blocks.vector_source_c(vector, repeat_onoff, 1, [])

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.osmosdr_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

def usage():
    print( "[--pulse_width { usecs }]\n")
    print( "[--pulse_interval { usecs}]\n")
    print( "[--pulse_count { number}]\n")
    print( "[--one_burst] # only one burst\n")
    print( "[--sweep_time { msec }]\n")
    print( "[--freq { khz }]\n")
    print( "[--daemon { 0 | 1 }]\n")
    print( "[--pid_file { pid-file-name }]\n")
    print( "[--gain {%s}]\n" % default_gain) # Main amp, on (14db) or off (0)
    print( "[--if_gain {%s} ]\n" % default_if_gain)  # Fine tune RX/TX gain, 0-40
    print( "[--bb_gain {%s} ]\n" % default_bb_gain)  # RX only 0-62, 2db steps
    print( "[--mgt_pipe { pipe-file-name}]  # To talk back to LANforge process\n")
    print( "[--help]\n\n")


def main(top_block_cls=top_block):
    pulse_width = 1
    pulse_interval = 1428
    pulse_count = 18
    one_burst = False # False = continuous
    sweep_time = 1000
    daemon = 0
    mgt_pipe_name = ""

    global gain
    global if_gain
    global bb_gain
    global vector
    global pid_file
    global mgt_pipe
    global freq
    global sample_mod

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "w:i:c:bs:f:d:m:p:g:a:v:h",
                                   ["pulse_width=", "pulse_interval=", "pulse_count=",
                                   "one_burst", "sweep_time=", "freq=", "daemon=",
                                   "mgt_pipe=", "pid_file=", "gain=", "if_gain=", "bb_gain=", "help" ])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-w", "--pulse_width"):
            pulse_width = int(a)
        elif o in ("-i", "--pulse_interval"):
            pulse_interval = int(a)
        elif o in ("-c", "--pulse_count"):
            pulse_count = int(a)
        elif o in ("-b", "--one_burst"):
            one_burst = True
        elif o in ("-s", "--sweep_time"):
            sweep_time = int(a)
        elif o in ("-d", "--daemon"):
            daemon = 1
        elif o in ("-m", "--mgt_pipe"):
            mgt_pipe_name = a;
        elif o in ("-p", "--pid_file"):
            pid_file = a;
        elif o in ("-f", "--freq"):
            freq = int(a) * 1000
        elif o in ("-g", "--gain"):
            gain = int(a)
        elif o in ("-a", "--if_gain"):
            if_gain = int(a)
        elif o in ("-v", "--bb_gain"):
            bb_gain = int(a)
        else:
            assert False, "unhandled option"

    killer = GracefulKiller()

    writePidFile()

    if mgt_pipe_name != "":
        mgt_pipe = open(mgt_pipe_name, "a")

    notifyMgr("starting")

    # Build our vector
    #pw = "[1]*%i" % (pulse_width)
    #pi = "[0]*%i" % (pulse_interval)
    #st = "[0]*%i" % (sweep_time * 1000)

    for i in range(0, pulse_count):
        vector += [1] * (pulse_width * sample_mod)
        vector += [0] * (pulse_interval * sample_mod)

    vector += [0]*((sweep_time * 1000 * sample_mod))

    #print vector

    tb = top_block_cls()

    if one_burst:
         tb.start()
         notifyMgr("started")
         # Give it time to run, very unlikely we have more than 1 sec of one-shot data
         time.sleep(1)

    else:
        tb.start()
        notifyMgr("started")
        while True:
           if daemon:
               # TODO:  Should ping hackrf device here to make sure everything
               # is working???
               if killer.kill_now:
                   break
               time.sleep(1)
               continue

           try:
               print( "Options: q(uit)  s(top)  g(o)\n")
               cmd = input('>>> ')
               if cmd == 'q':
                   break
               elif cmd == 's':
                   notifyMgr("stopping")
                   tb.stop()
                   tb.wait()
                   notifyMgr("stopped")
               elif cmd == 'g':
                   notifyMgr("starting")
                   tb.start()
                   notifyMgr("started")
               else:
                   print( "Options: q(uit)  s(top)  g(o)\n")
           except EOFError:
               break

    notifyMgr("stopping")
    tb.stop()
    notifyMgr("stopped")
    tb.wait()
    notifyMgr("exiting")

def notifyMgr(msg):
    global mgt_pipe

    if (mgt_pipe != -1):
        try:
            mgt_pipe.write("admin rfgen '%s'\n" % msg)
            mgt_pipe.flush()
            return
        except:
            pass
    print( msg + "\n")


def writePidFile():
    global pid_file

    pid = str(os.getpid())
    f = open(pid_file, 'w')
    f.write(pid)
    f.close()

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        print( "Stop signal received.\n")
        self.kill_now = True

if __name__ == '__main__':
    main()

