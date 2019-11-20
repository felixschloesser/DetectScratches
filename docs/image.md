# image.py
## load_img
Load and return an image-object from the given path.
### parameters:
 filename, size, color, array (either as a Pillow image object or numpy array)
### returns:
Pillow image object or numpy array


## save_img
Save an image array in the current working directory
### parameters:
array, filename, path

## img_list
Return a list of filenames for all jpg images in a directory.
### parameters:
path
### return:
list of strings

## resize_ing
Resize an image array using PIL.
### parameters:
img array, size tuple
### return:
img array

## show_hist
Display the Histogramm of a given Image
