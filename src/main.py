from PIL import Image as im
import os
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal as sg
from scipy.ndimage import filters, measurements, morphology, gaussian_laplace

from skimage.morphology import skeletonize, remove_small_objects, convex_hull_image
from skimage.measure import label, regionprops

from lib.image import load_img, show_img, show_hist, resize_img, save_img, img_list
from lib.edge import threshold, get_points, overlay_points
from lib.crop import mark_region, fit_lines, find_intersections, warp_to_corners

import argparse

parser = argparse.ArgumentParser(
    description='Read oearing images from /test_images, detect the number of scraches.')
parser.add_argument('-o','--output', help='Save the result images with marked scraches in /result_images',
                    action="store_true")

args = parser.parse_args()


# Insert the Path to the files you want to detect the scraches to here:
#path = "/home/tintin/rongheng/cv/test_images/"
path = "/Users/fs/Uni/Praktikum/DetectScratches/test_images/"

files  = list_imgs(path)

for file in files:
    raw_img = load_img(path + file, size=(300, 400))

    ## Cropped Image
    # Mark the border of the bearing using thresholgs
    border, scale = mark_region(raw_img)
    # The border img is resized so we can fit 4 clear lines to the sides.
    line_points = fit_lines(border, scale)
    intersections = find_intersections(line_points, raw_img.shape)
    img = warp_to_corners(raw_img, *intersections)


    ## Sobel edge detection
    def sobel(img, vert_weight=1, horr_weight=1):
        # Vertical Edges
        vert_edges = np.zeros(img.shape)
        filters.sobel(img, 1, vert_edges)

        # Horizontal Edges
        horr_edges = np.zeros(img.shape)
        filters.sobel(img, 0, horr_edges)

        # Magnitude
        magnitude = np.sqrt(vert_weight*vert_edges**2 + horr_weight*horr_edges**2)

        return magnitude


    response_img = sobel(img, vert_weight=1, horr_weight=0.6)


    ### Threshold and binary
    thresh_img = threshold(response_img, 0.38, False)
    binary_img = thresh_img.astype(bool)

    ## Connect neighboring regions
    # using first a morphological dialation to connect the neighboring regions and then skeletonizing
    #the regions again to end up with the precise markings.
    struct = morphology.generate_binary_structure(2, 2)
    dial_img = morphology.binary_dilation(binary_img, structure=struct, iterations=1)
    skeleton_img = skeletonize(dial_img)


    # ## Keep only the big scraches
    # We start by lableing all connected regions and sorting them by area (try eccentricity?).
    #We then only keep the ones that are bigger than a certain size.
    struct = morphology.generate_binary_structure(2,1)

    label_img = label(skeleton_img)
    scraches_img = remove_small_objects(label_img, 7)
    #regions = regionprops(label_img, coordinates='rc')
    #scraches = []
    #for region in regions:
    #    if region.eccentricity > 0.9 and region.area > 7:
    #        scrach = {'label':region.label, "area":region.area,
    #              'eccentricity':region.eccentricity}
    #        scraches.append(scrach)

    #scraches_list = [scrach.get("label") for scrach in scraches]
    #scraches_img = np.reshape([0 if label not in scraches_list else label
    #        for label in label_img.flatten()], label_img.shape)

    if args.output:
        ## Points on Image
        points = get_points(scraches_img, min_dist=0)
        # Extract the points from the result image and overlay them on the input image.
        fig = overlay_points(img, points)
        # Move one directory up

        # Check if results dir exists, if not create it.
        if not os.path.isdir("./results"):
            try: 
                os.chdir("../results")
            except:
                print("Could not find /results file, creating it.")
                os.mkdir("../results")

        print("saving results/" + file + "...")

        fig.savefig(file)
        plt.close(fig)


    srach_lables, num_of_scraches = measurements.label(scraches_img)
    print("Number of scraches in", file +":", num_of_scraches)





