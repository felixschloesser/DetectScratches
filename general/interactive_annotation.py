from PIL import Image
from pylab import *

file = 'oriental_pearl.jpg'

img = array(Image.open(file))
imshow(img)
print('Please click three points')
x = ginput(3)
print('You clicked: ', x)
show()