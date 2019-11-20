from bs4 import BeautifulSoup as Soup

import numpy as np
from scipy.ndimage import affine_transform
from PIL import Image
import os

import sys
sys.path.append("/home/tintin/rongheng/cv/")

from lib.image_lib import load_img, show_img, save_img

def read_points_xml(xml_filename):
    with open(xml_filename) as file:
        textfile = file.read()
    soup = Soup(textfile, 'xml')
    facelist = soup.find_all('face')

    faces = {}

    for face in facelist:
        filename = face['file']
        x_l = int(face['xf'])
        y_l = int(face['yf'])
        x_r = int(face['xs'])
        y_r = int(face['ys'])
        x_m = int(face['xm'])
        y_m = int(face['ym'])
        faces[filename] = [x_l, y_l,
                           x_r, y_r,
                           x_m, y_m]

    return faces


def rigit_transform(target, points):
    """
    Computes rotation, scale and translation for aligning points
    to refpoints.
    """
    A = np.array([[points[0], -points[1], 1, 0],
                  [points[1],  points[0], 1, 0],

                  [points[2], -points[3], 1, 0],
                  [points[3],  points[2], 1, 0],

                  [points[4], -points[5], 1, 0],
                  [points[5],  points[4], 1, 0]])

    b = np.array([target[0],
                 target[1],
                 target[2],
                 target[3],
                 target[4],
                 target[5]])


    # Least square solutuion to minimize Ax-b"
    a, b, tx, ty = np.linalg.lstsq(A,b, rcond=None)[0]
    R = np.array([[a, -b],[b, a]]) # rotation matrix incl scale

    return R, tx, ty



def rigid_alignment(faces, path):
    """
    Align images rigidly and save as new images. Path determines where
    aligned images are saved. set plotflag to plot the images.
    """
    # take the points in the first images as reference points
    reference_points = list(faces.values())[0]

    # warp each image using affine transform
    for face in faces:
        points = faces[face]

        R, tx, ty = rigit_transform(reference_points, points)
        T = np.array([[R[1][1], R[1][0]],
                  [R[0][1], R[0][0]]])

        try:
            img = np.array(Image.open(os.path.join(path,face)))
        except FileNotFoundError:
            print("skipping ",face, "...")
            continue
        img_2 = np.zeros(img.shape, 'uint8')

        # warp each color channel
        for i in range(len(img.shape)):
            img_2[:,:,i] = affine_transform(img[:,:,i], np.linalg.inv(T), offset=[-ty, -tx])

        # crop away border and save aligned image
        h, w = img_2.shape[:2]
        border = (w+h)//20

        #crop away border
        save_img(img_2[border:h-border, border:w-border,:], face, os.path.join(path + 'aligned/'))
