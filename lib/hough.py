import numpy as np

from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data

import matplotlib.pyplot as plt
from matplotlib import cm

from image_lib import load_img, show_img

import edge_lib as edge

from scipy.ndimage import morphology as morph_n

from skimage.filters import sobel
import skimage.feature as feature
import skimage.morphology as morph

from scipy import ndimage as nd


img = load_img('d02.jpg', size=(200, 200))

h, w = img.shape
size = h*w

markers = np.zeros_like(img)
markers[img > 255*0.05] = 1
markers[img > 255*0.6] = 0

erosion = morph_n.binary_erosion(markers, iterations=10)
labled, _ = nd.label(erosion)
bearing = morph.remove_small_objects(labled, size*0.2)
mask = morph.convex_hull_image(bearing)

inside = morph_n.binary_erosion(mask, iterations=4)
border = mask.astype(int) - inside.astype(int)
points = edge.get_points(border)

coords = [point[0] for point in points]
x = [coord[0] for coord in coords]
y = [coord[1] for coord in coords]

# Constructing test img
#img = np.zeros((100, 100))
#idx = np.arange(25, 75)
#img[idx[::-1], idx] = 255
#img[idx, idx] = 255

# Classic straight-line Hough transform
img = border
h, theta, d = hough_line(img)



# Generating figure 1
fig, axes = plt.subplots(1, 3, figsize=(25, 10))
ax = axes.ravel()

ax[0].imshow(img, cmap=cm.gray)
ax[0].set_title('Input img')
ax[0].set_axis_off()

ax[1].imshow(np.log(1 + h),
             extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]],
             cmap=cm.gray, aspect=1/10)
ax[1].set_title('Hough transform')
ax[1].set_xlabel('Angles (degrees)')
ax[1].set_ylabel('Distance (pixels)')
ax[1].axis('off')

ax[2].imshow(img, cmap=cm.gray)
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - img.shape[1] * np.cos(angle)) / np.sin(angle)
    ax[2].plot((0, img.shape[1]), (y0, y1), '-r')
ax[2].set_xlim((0, img.shape[1]))
ax[2].set_ylim((img.shape[0], 0))
ax[2].set_axis_off()
ax[2].set_title('Detected lines')

plt.tight_layout()
plt.show()
