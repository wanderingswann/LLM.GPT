# signals.py
import numpy as np
from scipy import signal

def generate_sine(num_samples, period, amplitude=1.0, phase_deg=0):
    phase_offset = phase_deg / 360 * period
    t = np.arange(num_samples)
    return amplitude * np.sin(2 * np.pi * (t - phase_offset) / period)

def generate_triangle(num_samples, period, amplitude=1.0, phase_deg=0):
    phase_offset = phase_deg / 360 * period
    t = np.arange(num_samples)
    return amplitude * signal.sawtooth(2 * np.pi * (t - phase_offset) / period, width=0.5)

def generate_square(num_samples, period, amplitude=1.0, phase_deg=0):
    phase_offset = phase_deg / 360 * period
    t = np.arange(num_samples)
    return amplitude * signal.square(2 * np.pi * (t - phase_offset) / period)

def generate_sawtooth(num_samples, period, amplitude=1.0, phase_deg=0):
    phase_offset = phase_deg / 360 * period
    t = np.arange(num_samples)
    return amplitude * signal.sawtooth(2 * np.pi * (t - phase_offset) / period)

def generate_unit_impulse(num_samples, impulse_position=0):
    impulse = np.zeros(num_samples)
    if 0 <= impulse_position < num_samples:
        impulse[impulse_position] = 1
    return impulse

def generate_unit_step(num_samples, step_position=0):
    t = np.arange(num_samples)
    return np.where(t >= step_position, 1, 0)
