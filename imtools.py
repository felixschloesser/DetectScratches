"""test."""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def img_list(path):
    """Return a list of filenames for all jpg images in a directory."""
    return [os.path.join(path, f) for f in os.listdir(path)
            if (f.endswith('.jpg') or f.endswith('.jpeg'))]


def resize_img(img, size):
    """Resize an image array unsing PIL."""
    img = Image.fromarray(np.uint8(img))

    return np.array(img.resize(size))


def eq_hist(img_array, num_bins=256):
    """Histogramm equilisation of a grayscale image."""
    hist, bins = plt.hist(img_array.flatten(), num_bins, density=True)
    cdf = hist.cumsum()  # cumulative dostribution function
    cdf = 255 * cdf / cdf[-1]  # normalize

    # use linar interpolation of cfg to find new pixel values
    im2 = plt.interp(img_array.flatten(), bins[:-1], cdf)

    return im2.reshape(img_array.shape)


def show_img(img, size=(5, 5), color=False):
    """Display an image given as an np.array."""
    plt.figure(figsize=size)
    if color:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
