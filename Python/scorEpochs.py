"""
 scorEpochs

 Function to select the best (most homogenoous) M/EEG epochs from a
 resting-state recordings.

 INPUT
    cfg: dictionary with the following key-value pairs
                 freqRange    - list with the frequency range used to compute the power spectrum
                                (see scipy.stats.spearmanr() function)
                 fs           - integer representing sample frequency
                 windowL      - integer representing the window length (in seconds)
                 smoothFactor - smoothing factor for the power spectrum

    data: 2d array with the time-series (channels X time samples)



 OUTPUT

    idx_best_ep: list of indexes sorted according to the best score (this list should be used for the selection of the
                  best epochs)

    epoch:       3d list of the data divided in equal length epochs of length windowL (channels X epochs X time samples)

    score_Xep:   array of score per epoch
"""

import numpy as np
from scipy import signal as sig
from scipy import stats as st

def scorEpochs(cfg, data):
    """
    :param cfg: dictionary with the following key-value pairs
                 freqRange    - list with the frequency range used to compute the power spectrum
                                (see scipy.stats.spearmanr() function)
                 fs           - integer representing sample frequency
                 windowL      - integer representing the window length (in seconds)
                 smoothFactor - smoothing factor for the power spectrum
    :param data: 2d array with the time-series (channels X time samples)

    :return:      idx_best_ep - list of indexes sorted according to the best score (this list should be used for the
                                selection of the best epochs)
                  epoch       - 3d list of the data divided in equal length epochs of length windowL
                                (channels X epochs X time samples)
                  score_Xep   - array of score per epoch
    """
    epLen = cfg['windowL'] * cfg['fs']
    dataLen = len(data[0])
    nCh = len(data)
    idx_ep = range(0, dataLen-epLen+1, epLen)
    nEp = len(idx_ep)
    epoch = np.zeros((nCh, nEp, epLen))
    freqRange = cfg['freqRange']
    smoothing_condition = 'smoothFactor' in cfg.keys() and cfg['smoothFactor'] > 1
    for e in range(nEp):
        for c in range(nCh):
            epoch[c][e] = data[c][idx_ep[e]: idx_ep[e] + epLen]
            # compute power spectrum
            f, aux_pxx = sig.welch(epoch[c][e], cfg['fs'], nperseg=cfg['windowL'], noverlap=0)
            if c == 0 and e == 0:
                idx_min = int(np.argmin(abs(f-freqRange[0])))
                idx_max = int(np.argmin(abs(f-freqRange[-1])))
                nFreq = len(aux_pxx[idx_min:idx_max+1])
                pxx = np.zeros((nCh, nEp, nFreq))
                if smoothing_condition:
                    window_range = round(cfg['smoothFactor'])
                    initial_f = int(window_range/2)
                    final_f = nFreq - initial_f
            pxx[c][e] = aux_pxx[idx_min:idx_max+1]
            if smoothing_condition:
                pxx[c][e] = _movmean(aux_pxx, cfg['smoothFactor'], initial_f, final_f, nFreq, idx_min, idx_max)

    pxxXch = np.zeros((nEp, len(pxx[0][0])))
    score_chXep = np.zeros((nCh, nEp))
    for c in range(nCh):
        for e in range(nEp):
            pxxXch[e] = pxx[c][e]

        score_ch, p = st.spearmanr(pxxXch)
        score_chXep[c] = np.mean(score_ch)
    score_Xep = np.mean(score_chXep, axis=1)
    idx_best_ep = np.argsort(score_Xep)
    idx_best_ep = idx_best_ep[::-1]
    return idx_best_ep, epoch, score_Xep


def _movmean(aux_pxx, smoothFactor, initial_f, final_f, nFreq, idx_min, idx_max):
    smoothed = np.zeros((idx_max-idx_min+1,))
    for f in range(nFreq):
        if f < initial_f:
            smoothed[f] = np.mean(aux_pxx[idx_min:idx_min+f+initial_f+1])
        elif f >= final_f:
            smoothed[f] = np.mean(aux_pxx[idx_min+f-initial_f:])
        elif smoothFactor % 2 == 0:
            smoothed[f] = np.mean(aux_pxx[idx_min+f-initial_f:idx_min+f+initial_f])
        else:
            smoothed[f] = np.mean(aux_pxx[idx_min+f-initial_f:idx_min+f+initial_f+1])
    return smoothed


if __name__ == "__main__":
    print("This function aims to select the best (most homogenoous) M/EEG epochs from a resting-state recordings.")
    print('\nThe only required arguments are the a dictionary, containing all the necessary pairs key-value, and the ',
          'time series.')
    print('The keys of the dictionary are: \n\t - freqRange: a list containing the initial and the final value of the ',
          'frequency band which has to be considered (in Hz) \n\t - fs: an integer representing the sampling frequency',
          ' (in Hz) \n\t - windowL: an integer representing the length of each epoch in which the time series has to ',
          'be divided (in seconds) \n\t - smoothFactor: the smoothing factor for the power spectrum (optional)')
    print('\nThe function returns a list containing the indexes of the best epochs, a 3d list containing the time ',
          'series divided in epochs (channels X epochs X time series), and the list of the scores assigned to each ',
          'epoch.')
    print('\n\nTaking for example a random time series of 10 channels and 10000 samples, contained in a 2d list ',
          '(10 X 10000), having a sampling frequency equal to 100 Hz, in order to evaluate the best epochs of 10 ',
          'seconds, studying the frequency band between 10 and 40 Hz, considering a smoothing factor (length of the ',
          ' window used by the moving average in the power spectrum), it is necessary to use the following dictionary:',
          "\n\t\t{'freqRange':[10, 40], 'fs':100, 'windowL':10, 'smoothFactor':3}")
    print('So, in order to execute the function using these parameters, it is possible to use:')
    print("idx_best, epoch, scores = scorEpochs({'freqRange':[10, 40], 'fs':100, 'windowL':10, 'smoothFactor':3}",
          ", time_series)")
    np.random.seed()
    time_series = np.zeros((10, 10000))
    x = np.linspace(1, 10000, 10000)
    for i in range(10):
        for j in range(10000):
            time_series[i][j] = np.random.normal(scale=1)
    idx_best, epoch, scores = scorEpochs({'freqRange':[10, 40], 'fs':100, 'windowL':10, 'smoothFactor':3}, time_series)
    print("\n\nAs result, idx_best contains the list of the best epochs:")
    print(idx_best)
    print("\nThe 3d list named epoch contains the original signal segmented in epochs (channels X epochs X time ",
          "series) and, in this case, it has the following dimensions:")
    print(str(len(epoch)) + " " + str(len(epoch[0])) + " " + str(len(epoch[0][0])))
    print("\nFinally, scores contains the score of each epoch:")
    print(scores)
    print("\n\nFor example, in order to extract the five best epochs, it is possible to execute: \n\t ")
    print("best_epochs = np.zeros((len(epoch), 5, len(epoch[0][0])))")
    print("for c in range(len(epoch)):")
    print("\tfor e in range(5):")
    print("\t\tbest_epochs[c][e] = epoch[c][idx_best[e]]")
    best_epochs = np.zeros((len(epoch), 5, len(epoch[0][0])))
    for c in range(len(epoch)):
        for e in range(5):
            best_epochs[c][e] = epoch[c][idx_best[e]]