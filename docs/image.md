# image.py

## list_img
Return a list of filenames for all jpg images in a directory.
### parameters:
path
### return:
list of strings

## load_img
Load and return an image-object from the given path.
### parameters:
 filename, size, color, array (either as a Pillow image object or numpy array)
### returns:
Pillow image object or numpy array


## save_img
Save an image array in the current working directory as a jpg.
### parameters:
array, filename, path

## show_img
Display one or multiple images given as an numpy array
### parameter:
one or many image arrays, size tuple, color, minimum value, maximum value



## resize_ing
Resize an image array using PIL.
### parameters:
image array, size tuple
### return:
image array

## show_hist
Display the Histogram of a given Image
### parameters:
image array, number of bins, size tuple

## eq_hist
Histogramm equilisation of a grayscale image using a cumulative distribution function.
### parameters:
image array, number of bins


