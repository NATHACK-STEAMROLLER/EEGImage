# -*- coding: utf-8 -*-
"""
Estimate Relaxation from Band Powers

This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.

The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al

Adapted from https://github.com/NeuroTechX/bci-workshop
"""

import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import random
from datetime import datetime
import os

# Handy little enum to make code more readable


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


""" EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0]

if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta]
    band_buffer = np.zeros((n_win_test, 4))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')

    try:
        now = datetime.now()
        start = now.strftime('%H:%M:%S')
        start_sec = int(start[0:2])*3600 + int(start[3:5])*60 + int(start[-2:])
        end_sec = start_sec + 22

        alpha = []
        beta = []
        delta = []
        theta = []
        relax = []

        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            now = datetime.now()
            cur_sec = now.strftime('%H:%M:%S')
            cur_sec = int(cur_sec[0:2]) * 3600 + int(cur_sec[3:5]) * 60 + int(cur_sec[-2:])
            if cur_sec == end_sec:
                break
            else:
                print(cur_sec)

            """ 3.1 ACQUIRE DATA """
            # Obtain EEG data from the LSL stream
            eeg_data, timestamp = inlet.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs))

            # Only keep the channel we're interested in
            ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

            # Update EEG buffer with the new data
            eeg_buffer, filter_state = utils.update_buffer(
                eeg_buffer, ch_data, notch=True,
                filter_state=filter_state)

            """ 3.2 COMPUTE BAND POWERS """
            # Get newest samples from the buffer
            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)

            # Compute band powers
            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))
            # Compute the average band powers for all epochs in buffer
            # This helps to smooth out noise
            smooth_band_powers = np.mean(band_buffer, axis=0)

            print('Delta: ', band_powers[Band.Delta], ' Theta: ', band_powers[Band.Theta], ' Alpha: ', band_powers[Band.Alpha], ' Beta: ', band_powers[Band.Beta])
            delta.append(band_powers[Band.Delta])
            theta.append(band_powers[Band.Theta])
            alpha.append(band_powers[Band.Alpha])
            beta.append(band_powers[Band.Beta])

            """ 3.3 COMPUTE NEUROFEEDBACK METRICS """
            # These metrics could also be used to drive brain-computer interfaces

            # Alpha Protocol:
            # Simple redout of alpha power, divided by delta waves in order to rule out noise
            alpha_metric = smooth_band_powers[Band.Alpha] / \
                smooth_band_powers[Band.Delta]
            print('Alpha Relaxation: ', alpha_metric)
            relax.append(alpha_metric)


            # Beta Protocol:
            # Beta waves have been used as a measure of mental activity and concentration
            # This beta over theta ratio is commonly used as neurofeedback for ADHD
            # beta_metric = smooth_band_powers[Band.Beta] / \
            #     smooth_band_powers[Band.Theta]
            # print('Beta Concentration: ', beta_metric)

            # Alpha/Theta Protocol:
            # This is another popular neurofeedback metric for stress reduction
            # Higher theta over alpha is supposedly associated with reduced anxiety
            # theta_metric = smooth_band_powers[Band.Theta] / \
            #     smooth_band_powers[Band.Alpha]
            # print('Theta Relaxation: ', theta_metric)

        mean_alpha = sum(alpha)/len(alpha)
        mean_beta = sum(beta)/len(beta)
        mean_delta = sum(delta)/len(delta)
        mean_theta = sum(theta)/len(theta)
        mean_relax = sum(relax)/len(relax)
        print('A ', mean_alpha, 'B ', mean_beta, 'd ', mean_delta, 't ', mean_theta, 'r ', mean_relax)

        path = '~/EEGImage/EEGImage/generateImage/static/prompt.txt'
        expanded = os.path.expanduser(path)
        with open(expanded, 'w') as f:
            if mean_relax >= 0.45:
                f.write(random.choice(['blue sky, ', 'blue ocean, ', 'mountain and sweet breeze, ', 'warm house, ']))
            else:
                f.write(random.choice(['dark place, ', 'cold and unpleasant winter, ', 'lurking beast, ']))

            if mean_theta + mean_alpha >= 1.1:
                f.write(random.choice(['relax, ', 'calm, ', 'creative state, ', 'comfortable, ', 'moon, ']))
                f.write(random.choice(['bright, ', 'cute animal, ', 'cute kids having fun, ', 'smiling face, ']))
            else:
                f.write(random.choice(['uncomfortable, ', 'distracted, ', 'unpleasant, ', 'embarrassing, ']))
                f.write(random.choice(['cliff, ', 'windy, ', 'cloudy, ', 'panic, ', 'sad, ', 'sigh, ', 'fox, ']))

            if mean_beta + mean_delta >= 1.1:
                f.write(random.choice(['alert, ', 'stressful, ', 'anxious, ', 'busy, ']))
                f.write(random.choice(['jail, ', 'dull, ', 'dangerous, ', 'raining, ', 'thundering, ', 'wolves, ']))
            else:
                f.write(random.choice(['cozy, ', 'hoodie,', 'snowing, ']))
                f.write(random.choice(['rabbit, ', 'hamster, ', 'squirrel, ']))

    except KeyboardInterrupt:
        print('Closing!')
