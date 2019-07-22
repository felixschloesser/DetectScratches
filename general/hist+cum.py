from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import imtools


def linear_trans(img_array):
    return img_array


def power_trans(img_array, pow):
    return 255.0 * (img_array/255.0)**pow


def eq_hist(img, num_bins = 256):
    """
    Histogramm equilisation of grayscale image
    """
    hist, bins, patches = plt.hist(img.flatten(), num_bins, cumulative=True)
    cdf = hist.cumsum()
    cdf = 255 * cdf / cdf[-1] # normalize
    
    img_2 = np.interp(img.flatten(), bins[:-1], cdf)
    plt.cla()

    return img_2.reshape(img.shape)



filename = 'bearing_soft.jpg'

img = Image.open(filename).convert('L')
img.thumbnail((512,512))
img_array = np.array(img, dtype='f')

space = np.linspace(0, 255, 255)


fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Histogramm', color=color)
ax1.hist(eq_hist(img_array).flatten(), bins= 256, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xlim([0,255])
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Cumulative Histogramm', color=color)  # we already handled the x-label with ax1
ax2.hist(eq_hist(img_array).flatten(), bins= 256, cumulative = True, histtype='step', color = color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()