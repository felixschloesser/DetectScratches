from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import imtools


def linear_trans(img_array):
    return img_array


def power_trans(img_array, pow=2):
    return 255.0 * (img_array/255.0)**pow


def eq_hist(img, num_bins = 256):
    """
    Histogramm equilisation of grayscale image
    """
    hist, bins, _ = plt.hist(img.flatten(), num_bins, density=True)
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
img_array = np.array(img)


# Plotting
fig, ax = plt.subplots(3,3, constrained_layout=True)

# pictues
ax[0, 0].imshow(linear_trans(img_array), cmap='gray', vmin=0, vmax=255)
ax[0, 1].imshow(power_trans(img_array), cmap='gray', vmin=0, vmax=255)
ax[0, 2].imshow(eq_hist(img_array), cmap='gray', vmin=0, vmax=255)

for i in range(3):
	ax[0, i].axis('off')

# transformations
ax[1, 0].plot(linear_trans(space), color='r')
ax[1, 0].set_ylim([0,255])
ax[1, 1].plot(power_trans(space), color='g')
ax[1, 1].set_ylim([0,255])
ax[1, 2].plot(eq_hist(space), color ='b')
ax[1, 2].set_ylim([0,255])


# Histograms
color = 'tab:blue'
color_culm = 'tab:red'

ax[2, 0].hist(linear_trans(img_array).flatten(), bins=256)
ax[2, 0].set_xlim([0,255])
ax[2, 0].set_ylim([0,8000])
ax20 = ax[2, 0].twinx()
ax20.hist(linear_trans(img_array).flatten(), bins=256, cumulative=True, density=True, histtype='step', color=color_culm)

ax[2, 1].hist(power_trans(img_array).flatten(), bins=256, color=color)
ax[2, 1].set_xlim([0,255])
ax[2, 1].set_ylim([0,8000])
ax21 = ax[2, 1].twinx()
ax21.hist(power_trans(img_array).flatten(), bins=256, cumulative=True, density=True, histtype='step', color=color_culm)

ax[2, 2].hist(eq_hist(img_array).flatten(), bins=256, color=color)
ax[2, 2].set_xlim([0,255])
ax[2, 2].set_ylim([0,8000])
ax22 = ax[2, 2].twinx()
ax22.hist(eq_hist(img_array).flatten(), bins=256, cumulative=True, density=True, histtype='step', color=color_culm)

plt.show(fig)