import numpy as np
import numpy.fft as fft

from scipy import signal as sg
from skimage import io

import sys
sys.path.append("/home/tintin/rongheng/cv/lib/")

from image_lib import load_img, show_img, show_hist, resize_img
from signal_lib import bandpass
from edge_lib import threshold

img = load_img("bearing_scrached_fuji_tunnel.jpg")
print(img.shape)

def bandpass_kernel(lowcut, highcut, transition, sample_frequency):
    bandpass_wavelet, length = bandpass(lowcut, highcut, transition, sample_frequency)
    bandpass_2d = np.outer(bandpass_wavelet, bandpass_wavelet)

    return bandpass_2d, length

#kernel, length = bandpass_kernel(500, 5, 1, sample_frequency=1000)
kernel, length = bandpass_kernel(500, 20, 1, sample_frequency=1000)
filtered_img = sg.convolve(kernel, img, 'full')
filtered_img = filtered_img[length:-length,length:-length]
thresh_img = threshold(filtered_img, -14, invert=True)

binary_img = np.where(thresh_img < 0, 1, 0)

show_img(filtered_img, size=(15,15), color="bwr", vmin=-20, vmax=20)
show_img(thresh_img, size=(15,15))
show_img(binary_filtered_img, size=(15,15))

#fourier_raw = fft.fft2(filtered_img)
#fourier_img = fft.fftshift(fourier_raw)
#show_img(filtered_img, (20*np.log10(0.1 + fourier_img)).astype(int), color="True", size=(25,25))
