# crop.py

## mark_region
Mark the approximate region of the bearing in a binary image using three intensity samples of the b/w image.
Do some morphological operations to separate the just the inner bearing and output it as a binary image. During this the image was also temporaily shrunken such that the hough lines operator is more accurate.
### parameters
image array
### return
image array of a thin border around the part, factor the image was scaled down by


## fit_lines
Fit four lines to each side of the binary image of the bearing approximating a rectangle.
### parameters
image array, scale factor
### return
tuple of to points for each of the for lines in a list


## find_intersections
Find the intersection of two straight lines.
### parameters
list tuples of two points on each line, image shape tuple
### return
coordinate tuples for top_left, bottom_left, top_right and bottom_right intersection in a list.


## warp_to_corners
take the coordinates of the four intersections as input and warp the image like so that they are at the corners of the image.
### parameters
image array, top_left, bottom_left, top_right, bottom_right coordinates.
### return
warped image array