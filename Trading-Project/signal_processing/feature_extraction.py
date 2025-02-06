# feature_extraction.py
import numpy as np

def compute_fft_features(signal_array):
    fft_vals = np.fft.fft(signal_array)
    fft_magnitude = np.abs(fft_vals)
    # We take only the positive frequencies
    half = len(signal_array) // 2
    return fft_magnitude[:half]

def rolling_snr(signal_array, window):
    import pandas as pd
    s = pd.Series(signal_array)
    # Calculate a simple moving average (mean) and standard deviation
    ma = s.rolling(window).mean()
    stdev = s.rolling(window).std()
    # Avoid division by zero by filling NaNs with a small number
    snr = ma / (stdev.replace(0, 1e-6))
    return snr.values
