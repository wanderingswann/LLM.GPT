# filters.py
import numpy as np

def sma_filter(signal_array, window):
    kernel = np.ones(window) / window
    return np.convolve(signal_array, kernel, mode='same')

def ema_filter(signal_array, length):
    alpha = 2 / (length + 1)
    ema = np.zeros_like(signal_array)
    ema[0] = signal_array[0]
    for i in range(1, len(signal_array)):
        ema[i] = alpha * signal_array[i] + (1 - alpha) * ema[i-1]
    return ema

def fir_filter(signal_array, kernel):
    # Assume kernel is pre-normalized (i.e., sum(kernel) == 1)
    return np.convolve(signal_array, kernel, mode='same')
