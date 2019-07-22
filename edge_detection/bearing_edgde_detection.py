"""Detect the edges in a bearing image."""

import numpy as np
import edge_detection as edg
import imtools
from PIL import Image

filename = 'bearing_scrached_fuji_tunnel'
img = Image.open('../test_images/' + filename).convert(L)
img = np.array(img)