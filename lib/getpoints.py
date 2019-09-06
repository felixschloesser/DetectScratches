
from image_lib import load_img, show_img
from edge_lib import get_points, overlay_points
from skimage import filters
import numpy as np

img = load_img("d01.jpg", size=(200,200))
edges = filters.sobel(img)
points = get_points(edges, threshold=0.2,min_dist=1)
filtered_points = overlay_points(img, points)

