"""Functions to calculate image derivatives."""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg
import scipy.ndimage as filters


def threshold(img, threshold):
    """Replace all values bellow a given threshold in an np.array with 0."""
    img = np.where(img > threshold, 255, 0)

    return img


def gaussian_kernel(n, std, normalised=False):
    """
    Generate a n x n matrix with a gaussian centered on it.

    The distributions standard dev is std. If normalised, its volume equals 1.
    """
    gaussian = sg.gaussian(n, std)
    gaussian2d = np.outer(gaussian, gaussian)

    if normalised:
        gaussian2d /= (2 * np.pi * (std**2))

    return gaussian2d


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


def get_points(response, min_dist=10, threshold_percent=0.1):
    """
    Return corners from a Harris response image.

    min_dist ist the minumum number of pixels seperating corners
    and image boundary.
    """
    # find top corner caditades above a threshold
    threshold = response.max() * threshold_percent
    response_threshold = threshold(response, threshold)

    # get coordinates of candidates
    coords = np.array(response_threshold.nonzero()).T

    # ... and their values
    candidate_values = [response[c[0], c[1]] for c in coords]

    # sort candidates
    index = np.argsort(candidate_values)

    # store allowed point locations in array
    allowed_locations = np.zeros(response.shape)
    allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 1

    # select the best points taking min_distance into account
    filtered_coords = []

    for i in index:
        if allowed_locations[coords[i, 0], coords[i, 1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i, 0] - min_dist):
                              (coords[i, 0] + min_dist),

                              (coords[i, 1] - min_dist):
                              (coords[i, 1] + min_dist)] = 0

    return filtered_coords


def plot_points(image, filtered_coords, save=False):
    """Plot corners found in image."""
    plt.figure(figsize=(15, 15))
    plt.imshow(image)
    plt.plot([p[1] for p in filtered_coords], [p[0] for p in filtered_coords],
             'r*')
    plt.axis('off')
    plt.title('edge points')
    if save:
        plt.savefig('result_images/edge_points.jpg')
