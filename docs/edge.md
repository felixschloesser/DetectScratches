# edge.py

## threshold
Replace all values in a given image array bellow a given threshold with 0 rest 255. This binarizes the image effectively. Instead of an absolute value, a percent of the image values can also be chosen.
### parameters
image, threshold value, boolean percent, boolean invert
### return
image array

## derivative
Calculate the derivative of an image in a given direction. This realizes a simple edge detector using with a convolution of the first derivative of the gaussian normal distribution function. More information: https://en.wikipedia.org/wiki/Image_derivatives
### parameters
image array, direction [x-direction, y-direction, both (magnitude)], sigma value for the normal distribution

## harris_response
Compute the Harris corner detector response matrix of a graylevel image. 
More information: https://en.wikipedia.org/wiki/Corner_detection#Harris_corner
### parameters
image array, sigma value
### return
image array

## get_points
Return coordinates of the points on a image that are non zero as a dictionary, by default sorted by value in the array. If min_distance is set ignore other points in the vicinity.
### parameters
image array, boolean sort, minimum distance
### return
image array

## overlay_points
Plot the points in red using the coordinates on the given image.
### parameters
image array, list of coordinate tuples, size tuple
### return
figure