import numpy as np
import itertools as it
import matplotlib.pyplot as plt

from scipy.ndimage import morphology, measurements

from skimage.morphology import remove_small_objects, convex_hull_image
from skimage.measure import label
from skimage.transform import hough_line, hough_line_peaks, ProjectiveTransform, warp

from lib.image import resize_img

def mark_region(img):
    # Make smaller so that hough lines later always finds the right 4 lines
    height, width = (150, 200)
    size = height*width
    img, scale = resize_img(img, (height, width))

    markers = np.zeros_like(img)
    markers[img > 255*0.05] = 1
    markers[img > 255*0.6] = 0

    erosion = morphology.binary_erosion(markers, iterations=10)
    labled, _ = measurements.label(erosion)
    bearing = remove_small_objects(labled, size*0.2)
    mask = convex_hull_image(bearing)
    inside = morphology.binary_erosion(mask, iterations=4)
    border = mask.astype(int) - inside.astype(int)

    return border, scale


def fit_lines(border, scale):
    h, theta, d = hough_line(border)
    hough_lines = zip(*hough_line_peaks(h, theta, d))
    lines = []

    def line_points(angle, dist, border):
        _, width = border.shape
        line_equation = lambda x: (dist - x * np.cos(angle))/np.sin(angle)
        p1, p2 = [(x, line_equation(x)) for x in np.linspace(0, width/scale, 2)]

        return p1, p2

    for _, angle, dist in hough_lines:
        # Scale back the Lines
        dist = dist * 1/scale
        l = line_points(angle, dist, border)

        lines.append(l)

    return lines



def find_intersections(line_points, shape):
    height, width = shape
    def line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])

        return A, B, -C

    def intersect(L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            if 0 < x <= width and 0 < y <= height:
                return x,y
        else:
            return False

    lines_permut = list(it.combinations(line_points, 2))
    intersections = []

    for l1, l2 in lines_permut:
        L1 = line(*l1)
        L2 = line(*l2)
        r = intersect(L1, L2)
        if r:
            intersections.append(r)

    intersections.sort(key= lambda x: (x[0] + x[1]))
    top_left = intersections.pop(0)
    bottom_right = intersections.pop()
    intersections.sort(key= lambda x: (x[0]))
    top_right = intersections.pop()
    bottom_left = intersections.pop(0)

    return top_left, bottom_left, top_right, bottom_right


def warp_to_corners(img, top_left, bottom_left, top_right, bottom_right):
    height, width = img.shape

    src = np.array([[0, 0], [0, height], [width, height], [width, 0]])
    dst = np.array([top_left, bottom_left, bottom_right, top_right])

    tform3 = ProjectiveTransform()
    tform3.estimate(src, dst)

    new_shape = (int(height*0.8), int(width*0.8))
    warped = warp(img, tform3, output_shape=img.shape)

    return warped
