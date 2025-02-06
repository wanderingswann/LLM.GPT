# dataset_builder.py
import numpy as np
from signal_processing import signals, filters, feature_extraction

def build_dataset(signal_type_func, num_samples=500, period=50, amplitude=1.0, phase_deg=0, window_length=100, num_windows=100):
    """
    Generate a dataset from a signal type. For each sample, a window of data is taken and features are extracted.
    signal_type_func: function to generate the signal (e.g., signals.generate_sine)
    """
    dataset = []
    labels = []
    
    for _ in range(num_windows):
        # You can add randomness to parameters if desired:
        period_sample = period + np.random.randint(-5, 6)
        amplitude_sample = amplitude * (1 + np.random.uniform(-0.1, 0.1))
        phase_sample = phase_deg + np.random.uniform(-10, 10)
        
        sig = signal_type_func(num_samples, period_sample, amplitude_sample, phase_sample)
        
        # Example: extract the first window_length samples as a feature vector.
        window = sig[:window_length]
        
        # Optionally, you can extract more features such as FFT features or SNR.
        fft_feats = feature_extraction.compute_fft_features(window)
        snr_feat = np.mean(feature_extraction.rolling_snr(window, window=10))
        
        # Concatenate raw window, FFT features, and SNR as one feature vector.
        feature_vector = np.concatenate([window, fft_feats, [snr_feat]])
        dataset.append(feature_vector)
        labels.append(signal_type_func.__name__)  # label by the function name, for example
    
    return np.array(dataset), np.array(labels)
