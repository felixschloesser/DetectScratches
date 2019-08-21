import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def load_img(filename, size=(512, 512), color=False, array=True):
    """Load and return an image-object from the standard path."""
    test_images_path = '/home/tintin/rongheng/cv/test_images/'
    os.chdir(test_images_path)
    img = Image.open(filename)

    img.thumbnail(size)

    if not color:
        # convert to grayscale
        img = img.convert('L')

    if array:
        # return as np.array
        img_array = np.array(img)
        return img_array
    else:
        # return as Pillow.Image
        return img


def save_img(array, filename):
    path = "/home/tintin/rongheng/cv/result_images/"
    Image.fromarray(array.round().astype(np.uint8)).save(path + filename)


def img_list(path):
    """Return a list of filenames for all jpg images in a directory."""
    return [os.path.join(path, f) for f in os.listdir(path)
            if (f.endswith('.jpg') or f.endswith('.jpeg'))]


def resize_img(img, size):
    """Resize an image array unsing PIL."""
    img = Image.fromarray(np.uint8(img))

    return np.array(img.resize(size))


def show_hist(img_array, num_bins=256, size=(5, 5)):
    """Display the Histogramm of a givin Image."""
    plt.figure(figsize=size)
    plt.hist(img_array.flatten(), num_bins)

    plt.show()


def eq_hist(img_array, num_bins=256):
    """Histogramm equilisation of a grayscale image."""
    hist, bins = plt.hist(img_array.flatten(), num_bins, density=True)
    cdf = hist.cumsum()  # cumulative dostribution function
    cdf = 255 * cdf / cdf[-1]  # normalize

    # use linar interpolation of cfg to find new pixel values
    im2 = plt.interp(img_array.flatten(), bins[:-1], cdf)

    return im2.reshape(img_array.shape)


def show_img(*images, size=(10, 10), color="", vmin=0, vmax=255):
    """Display one or multiple images given as an np.array."""
    image = (i for i in images)
    rows = int(np.round(np.sqrt(len(images))))
    columns = int(np.ceil(np.sqrt(len(images))))

    fig, grid = plt.subplots(rows, columns, squeeze=False,figsize=size)
    frames = [frame for row in grid for frame in row]
    for frame in frames:
        frame.axis("off")
        try:
            if not color:
                frame.imshow(next(image))
            elif color == "bw":
                frame.imshow(next(image), cmap="gray", vmin=vmin, vmax=vmax)
            else:
                frame.imshow(next(image), cmap=color, vmin=vmin, vmax=vmax)
        except StopIteration:
            break
    plt.show()


def normalize(img):
    normalized = 255. * np.absolute(img) / np.max(img)

    return normalized
