import numpy as np

import sys
sys.path.append("/home/tintin/rongheng/cv/")
from lib.image_lib import show_img, load_img
import lib.edge_lib as edge

from scipy.ndimage import morphology as morph_n

from skimage.filters import sobel
import skimage.feature as feature
import skimage.morphology as morph

from scipy import ndimage as nd


img = load_img('d01.jpg', size=(800, 800))

h, w = img.shape
size = h*w

markers = np.zeros_like(img)
markers[img > 255*0.05] = 1
markers[img > 255*0.6] = 0

erosion = morph_n.binary_erosion(markers, iterations=20)

labled, _ = nd.label(erosion)

bearing = morph.remove_small_objects(labled, size*0.2)

mask = morph.convex_hull_image(bearing)

inside = morph_n.binary_erosion(mask, iterations=4)
border = mask.astype(int) - inside.astype(int)
points = edge.get_points(border)

import matplotlib.pyplot as plt

coords = [point[0] for point in points]
x = [coord[0] for coord in coords]
y = [coord[1] for coord in coords]

plt.plot(x, y, "r*")
plt.show()



