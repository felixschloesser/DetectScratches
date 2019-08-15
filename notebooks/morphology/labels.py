import math
import matplotlib.pyplot as plt
import numpy as np

from scipy import signal as sg

import skimage.measure as measure
from skimage.draw import ellipse
from skimage.transform import rotate

import sys
sys.path.append("/home/tintin/rongheng/cv/")
from lib.image_lib import load_img, show_img, show_hist, resize_img, save_img
from lib.signal_lib import bandpass
from lib.edge_lib import threshold

def bandpass_kernel(lowcut, highcut, transition, sample_frequency):
    bandpass_wavelet, length = bandpass(lowcut, highcut, transition, sample_frequency)
    bandpass_2d = np.outer(bandpass_wavelet, bandpass_wavelet)

    return bandpass_2d, length

img = load_img("bearing_scrached_fuji_tunnel.jpg")

kernel, length = bandpass_kernel(500, 5, 1, sample_frequency=1000)
filtered_img = sg.convolve(kernel, img, 'full')
filtered_img = filtered_img[length:-length,length:-length]
filtered_img = threshold(filtered_img, -5.5, invert=True)

show_img(filtered_img, size=(10,10), color="bwr", vmin=-20, vmax=20)

label_img = measure.label(filtered_img)
show_img(filtered_img, label_img,size=(15,10))
