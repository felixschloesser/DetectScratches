import numpy as np
import matplotlib.pyplot as plt


def plot_signal(sig, amp, sample_frequency, title=""):
    time = np.linspace(0, 2*np.pi, sample_frequency, endpoint=True)

    plt.figure(figsize=(10,2))
    plt.plot(time,sig)
    plt.ylim((-amp,+amp))
    plt.xlabel("Time ($s$)")
    plt.ylabel("Aplitude ($Unit$)")
    if title:
        plt.title(title)


def plot_fourier(signal, sample_frequency, size=(10,4), title=""):
    time = np.linspace(0, 2*np.pi, sample_frequency, endpoint=True)


    window = np.blackman(len(signal))

    response = np.fft.fft(window*signal)

    N = len(response) // 2
    delta_t = time[1] - time[0] #
    f_a = 1 / delta_t
    f_nyquist = f_a / 2

    freq_vec = np.linspace(0, f_nyquist, N, endpoint=True)

    plt.figure(figsize=size)
    plt.plot(freq_vec, 2.0*np.abs(response[:N])/N)
    plt.xlabel("Frequency ($Hz$)")
    plt.ylabel("Amplitude ($Unit$)")
    if title:
        plt.title(title)
    else:
        plt.title("Frequency Domain")

    plt.show()


def lowpass(cutoff, transition, sample_frequency):
    f_c = cutoff / sample_frequency
    t_band = transition / sample_frequency  # Transition band

    N = int(np.ceil((4 / t_band))) # Filter length
    if not N % 2: N += 1  # Make sure that N is odd.
    print("Filter Length =",N)
    n = np.arange(N)

    # Compute sinc filter.
    h = np.sinc(2 * f_c * (n - (N - 1) / 2))

    # Blackman window
    w = np.blackman(N)

    # Multiply filter by window.
    h = h * w

    # Normalize to get unity gain.
    h = h / np.sum(h)

    return h, N


def lowpass_filter(signal, cutoff, transition, sample_frequency = 1000):
    h, length = highpass(signal, cutoff, transition, sample_frequency)
    filtered_signal = np.convolve(signal, h)

    # Cutoff ends
    filtered_signal = filtered_signal[length//2-1:-length//2]

    return filtered_signal


def highpass(cutoff, transition, sample_frequency):
    f_c = cutoff / sample_frequency
    t_band = transition / sample_frequency  # Transition band

    N = int(np.ceil((4 / t_band))) # Filter length
    if not N % 2: N += 1  # Make sure that N is odd.
    print("Filter Length =",N)
    n = np.arange(N)

    # Compute sinc filter.
    h = np.sinc(2 * f_c * (n - (N - 1) / 2))

    # Blackman window
    w = np.blackman(N)

    # Multiply filter by window.
    h = h * w

    # Normalize to get unity gain.
    h = h / np.sum(h)

    # Perform spectral inversion to turn low_pass into high pass
    h = -h
    h[(N-1) // 2] += 1

    return h, N

def highpass_filter(signal, cutoff_frequency, transition_band, sample_frequency = 1000):
    h , length = highpass(signal, cutoff_frequency, transition_band, sample_frequency)
    filtered_signal = np.convolve(signal, h)

    # Cutoff ends
    filtered_signal = filtered_signal[length//2-1:-length//2]

    return filtered_signal


def bandpass(lowcut, highcut, transition, sample_frequency):
    f_cl = lowcut / sample_frequency
    f_ch = highcut / sample_frequency
    t_band = transition / sample_frequency  # Transition band

    N = int(np.ceil((4 / t_band))) # Filter length
    if not N % 2: N += 1  # Make sure that N is odd.
    print("Filter Length =",N)

    # Low-Pass with cutoff f_cl
    n = np.arange(N)
    h_lp = np.sinc(2 * f_cl * (n - (N - 1) / 2))
    w = np.blackman(N) # Blackman window
    h_lp = h_lp * w # Multiply filter by window.
    h_lp = h_lp / np.sum(h_lp) # Normalize to get unity gain.


    # High-Pass with cutoff f_cl
    n = np.arange(N)
    h_hp = np.sinc(2 * f_ch * (n - (N - 1) / 2))
    w = np.blackman(N) # Blackman window
    h_hp = h_hp * w # Multiply filter by window.
    h_hp = h_hp / np.sum(h_hp) # Normalize to get unity gain.
    h_hp = -h_hp # Perform spectral inversion to turn low_pass into high pass
    h_hp[(N-1) // 2] += 1

    h = np.convolve(h_lp, h_hp)

    return h, N

def bandpass_filter(signal, lowcut, highcut, transition, sample_frequency = 1000):
    h, length = bandpass(signal, cutoff_frequency, transition_band, sample_frequency)

    filtered_signal = np.convolve(signal, h)

    # Cutoff ends
    filtered_signal = filtered_signal[length//2-1:-length//2]

    return filtered_signal
