"""Functions to calculate image derivatives."""

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as filters


def threshold(img, threshold, percent=False, invert=False):
    if percent:
        threshold = img.max() * threshold

    """Replace all values bellow a given threshold with 0 rest 255."""
    if invert:
        binary_img = np.where(img >= threshold, 0, 255)
    else:
        binary_img = np.where(img <= threshold, 0, 255)

    return binary_img


def derivative(img, dir='xy', sigma=1):
    """Calculate the derivative of an image in a given direction."""
    direction = {'x': (0, 1), 'y': (0, 1), 'xy': 'magnitude'}

    if direction[dir] is 'magnitude':
        filters.gaussian_filter(img, (sigma, sigma), direction['x'],
                                np.zeros(img.shape))
        filters.gaussian_filter(img, (sigma, sigma), direction['y'],
                                np.zeros(img.shape))
    else:
        filters.gaussian_filter(img, (sigma, sigma), direction[dir],
                                np.zeros(img.shape))


def harris_response(img, sigma=3):
    """
    Compute the Harris corner detector response matrix.

    The function for each pixel in a graylevel image.
    """
    # derivatives
    img_x = np.zeros(img.shape)
    filters.gaussian_filter(img, (sigma, sigma), (0, 1), img_x)

    img_y = np.zeros(img.shape)
    filters.gaussian_filter(img, (sigma, sigma), (1, 0), img_y)

    # compute components of the harris matrix
    w_xx = filters.gaussian_filter(img_x * img_x, sigma)
    w_xy = filters.gaussian_filter(img_x * img_y, sigma)
    w_yy = filters.gaussian_filter(img_y * img_y, sigma)

    # determinant and trace
    w_det = w_xx * w_yy - w_xy**2
    w_thr = w_xx + w_yy

    return w_det / w_thr


def get_points(response, min_dist=10, allow_cluster=True):
    """
    Return corners from a response image.

    min_dist ist the minumum number of pixels seperating corners
    and image boundary.
    """

    # get coordinates of candidates
    coords = np.array(response.nonzero()).T

    # ... and their values
    candidate_values = [response[c[0], c[1]] for c in coords]

    # sort candidates
    index = np.argsort(candidate_values)

    # store allowed point locations in array
    allowed_locations = np.ones(response.shape)
    allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 0

    if allow_cluster:
        min_dist = 0

    # select the best points taking min_distance into account
    filtered_coords = []

    for i in index:
        if allowed_locations[coords[i, 0], coords[i, 1]] == 0:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i, 0] - min_dist):
                              (coords[i, 0] + min_dist),

                              (coords[i, 1] - min_dist):
                              (coords[i, 1] + min_dist)] = 1

    return filtered_coords


def overlay_points(image, filtered_coords, size=(15, 15), save=False):
    """Plot points found in image."""
    plt.figure(figsize=size)
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.plot([p[1] for p in filtered_coords], [p[0] for p in filtered_coords],
             'r*')
    plt.axis('off')
    plt.title('edge points')
    if save:
        plt.savefig('redge_points.jpg')

    plt.show()

