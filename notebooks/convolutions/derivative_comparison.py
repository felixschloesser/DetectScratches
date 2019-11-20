import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import filters
import sys
sys.path.append("/home/tintin/rongheng/cv/")
from imtools import *
from edge_detection import *


img = load_img('bearing_scrached_fuji_tunnel.jpg')

# Sobel deriviative filters

sigmas = [1, 2, 5, 10]
derivatives = {'img_x': (0, 1), 'img_y': (1, 0), 'gradient': 'magnitude'}

img_x = np.zeros(img.shape)
img_y = np.zeros(img.shape)


fig, frame = plt.subplots(len(derivatives), len(sigmas), figsize=(5, 5))

for i, sigma in enumerate(sigmas):
    img_blurred = filters.gaussian_filter(img, sigma)

    for j, derivative in enumerate(derivatives):
        if derivatives[derivative] == 'magnitude':
            filters.gaussian_filter(img_blurred, (sigma, sigma),
                                    derivatives['img_x'], img_x)
            filters.gaussian_filter(img_blurred, (sigma, sigma),
                                    derivatives['img_y'], img_y)
            magnitude = np.sqrt(img_x**2 + img_y**2)
            img_derivative = magnitude
        else:
            filters.gaussian_filter(img_blurred, (sigma, sigma),
                                    derivatives[derivative], img_x)
            img_derivative = img_x

        frame[j, i].imshow(img_derivative)
        frame[j, i].axis('off')
        frame[j, i].set_title(' sigma = ' + str(sigma))

plt.tight_layout()
plt.show()