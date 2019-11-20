"""Functions to calculate image derivatives."""

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as filters


def threshold(img, threshold, percent=False, invert=False):
    if percent:
        threshold = img.max() * threshold

    """Replace all values bellow a given threshold with 0 rest 255."""
    if invert:
        thresholded_img = np.where(img >= threshold, 0, img)
    else:
        thresholded_img = np.where(img <= threshold, 0, img)

    return thresholded_img


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



def get_points(array, sort=True, min_dist=0):
    """
    Return coordinates of the points on a image that are non zero as a 
    dictionary, by default sorted by value in the array. 
    If min_distance is set ignore other points in the vicinity.
    """

    # get coordinates of entries that are non zero
    coords = [tuple(c) for c in np.argwhere(array>0)]
    # ... and their values
    values = [array[x, y] for x,y in coords]

    points = []

    for i, value in enumerate(values):
        points.append(tuple([coords[i], value]))

    if sort:
        points.sort(key=lambda point: point[1], reverse=True)

    if min_dist:
        # store allowed point locations in array
        allowed_locations = np.ones(array.shape)
         # not on the edges of the image
        allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 0

        # select the best points taking min_distance into account
        filtered_points = []

        for point in points:
            x,y = point[0]

            if allowed_locations[x,y] == 0:
                filtered_points.append(point)
                allowed_locations[(x - min_dist):
                                  (x + min_dist),

                                  (y - min_dist):
                                  (y + min_dist)] = 1

            points = filtered_points
    return points


def overlay_points(image, points, size=(15, 15)):
    """
    Plot the points in red using the coordinates on the given image.
    """
    
    fig, ax = plt.subplots(figsize=size)
    ax.imshow(image)
    for point in points:
        x, y = point[0]
        plt.plot(y,x,'r*')
    ax.axis('off')

    return fig

