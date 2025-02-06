# main.py
import pandas as pd
import numpy as np
from signal_processing import signals, filters, feature_extraction, dataset_builder

def main():
    # Example: Load historical market data (adjust file path and column names as needed)
    data = pd.read_csv('data/historical_prices.csv')
    prices = data['close'].values

    # Pre-process market prices with filters
    sma_prices = filters.sma_filter(prices, window=10)
    ema_prices = filters.ema_filter(prices, length=20)

    # Generate and visualize a synthetic signal (optional)
    import matplotlib.pyplot as plt
    sine_signal = signals.generate_sine(num_samples=500, period=50, amplitude=1, phase_deg=30)
    plt.figure(figsize=(10,4))
    plt.plot(sine_signal, label='Sine Signal')
    plt.plot(sma_prices[:500], label='SMA on Prices', alpha=0.7)
    plt.legend()
    plt.title("Synthetic Signal and Filtered Prices")
    plt.show()

    # Feature extraction for ML: Build a dataset from one type of signal
    X, y = dataset_builder.build_dataset(
        signal_type_func=signals.generate_sine,
        num_samples=500,
        period=50,
        amplitude=1,
        phase_deg=30,
        window_length=100,
        num_windows=100
    )
    print("Dataset shape:", X.shape)
    print("Labels sample:", y[:5])
    
    # At this point, X and y can be fed into your machine learning model for training or prediction.
    # For example, you might save the dataset for later use:
    np.save('data/features.npy', X)
    np.save('data/labels.npy', y)
    
    # ... or directly train a model here.
    
if __name__ == '__main__':
    main()
