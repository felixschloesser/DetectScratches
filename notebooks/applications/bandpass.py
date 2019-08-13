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


kernel, length = bandpass_kernel(500, 5, 1, sample_frequency=1000)
filtered_img = sg.convolve(kernel, img, 'full')
filtered_img = filtered_img[length:-length,length:-length]
filtered_img = threshold(filtered_img, -5.5, invert=True)

io.imshow(filtered_img)
io.show()
print(filtered_img.shape)

#fourier_raw = fft.fft2(filtered_img)
#fourier_img = fft.fftshift(fourier_raw)
#show_img(filtered_img, (20*np.log10(0.1 + fourier_img)).astype(int), color="True", size=(25,25))
