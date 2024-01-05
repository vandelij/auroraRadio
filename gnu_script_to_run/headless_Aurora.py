#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Headless GNU Radio script for aurora freq.
# Author: Jacob van de Lindt
# GNU Radio version: 3.10.5.1

########
# New Stuff to Add: TODO: add to gnu radio code output
import datetime
import os
# End new stuff to Add: TODO: add to gnu radio code output

from gnuradio import audio
from gnuradio import blocks
import math
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time




class headless_FM(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Headless GNU Radio script for aurora freq.", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2400000
        self.center_freq = center_freq = 125000000
        self.Volume = Volume = .5

        ##################################################
        # Blocks
        ##################################################

        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=50,
                taps=[],
                fractional_bw=0)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(Volume)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*(-center_freq)/samp_rate)
        # New line of code TODO: ADD TO GNU RADIO OUTPUT
        now = datetime.datetime.now() 
        now.strftime("%Y-%m-%d %H:%M:%S")
        date_and_time = now.strftime("%Y_%m_%d__%H_%M_%S")
        save_directory = '/home/vandelij/Desktop/Aurora_Radio/test_recordings/'
        save_file_name = save_directory + 'aurora_radio_recording_date_EST_' + date_and_time
        print('PWD:')  
        print(os.getcwd())
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, save_file_name, False)
        # End new line of code TODO: ADD TO GNU RADIO OUTPUT
        #self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'sunriver_radio', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            12,
            firdes.band_pass(
                1,
                samp_rate,
                400,
                16000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_mag_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 400, 16000, 1000, window.WIN_HAMMING, 6.76))
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(-self.center_freq)/self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*(-self.center_freq)/self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)

    def get_Volume(self):
        return self.Volume

    def set_Volume(self, Volume):
        self.Volume = Volume
        self.blocks_multiply_const_vxx_0.set_k(self.Volume)




def main(top_block_cls=headless_FM, options=None):
    print('The headless pid is: ', os.getpid())
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    # try:
    #     input('Press Enter to quit: ')
    # except EOFError:
    #     pass
    # tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
