# Detect Scratches
Experiments into the field of computer vision done at my three month internship at Rongheng Information Technology Co. Ltd. in Shanghai.

## Requirements:
* numpy
* matplotlib
* Pillow
* scipy

see docker/requirements-full.txt for the full list

## Python only deployment:
* Clone the repository: `git clone https://github.com/felixschloesser/DetectScratches.git`
* Enter the directory: `cd DetectScratches/docker`
* Download the dependencies using `pip`: `pip install -r requirements-full.txt`
* Make sure the images you want to inspect are in the `test-images/`directory
* Execute using `./src/main.py`

You can use the `-o` flag to output the result images.


## Docker deployment:
Clone the repository using `git clone https://github.com/felixschloesser/DetectScratches.git`

Enter the directory: `cd DetectScratches/docker`

All you have to do is adjust binding path inside the docker-compose.yml to your cloned notebook folder.

Docker will take care of the rest for you :)
`docker-compose up`
Now you can navigate to http://127.0.0.1/:8888 to access the jupyter notebook.

Have fun!

------------------------------------------------------------------------------------------------------------

## Documentation

Development Environment: Jupyter Notebook

### Required Libaries:

* lib/image.py: [doc](/docs/image.md)
* lib/edge.py: [doc](/docs/edge.md)
* lib/crop.py: [doc](/docs/crop.md)

### Unused Libraries:

* lib/signal.py

## External Libraries:
For questions about external libraries, please read the corresponding documentation. I have linked them below.

* **NumPy**: [docs](https://numpy.org/doc/)
* **scipy**: [docs](https://docs.scipy.org/doc/scipy/reference/)
* **Pillow**: [docs](https://pillow.readthedocs.io/en/stable/)
* **matplotlib**: [docs](https://matplotlib.org/contents.html)
* **scikit-image**: [docs](https://scikit-image.org/docs/stable/)
* **ipywidgets**: [docs](https://ipywidgets.readthedocs.io/en/latest/)



# Literature
* Programming Computer Vision, O'Reilly, ISBN: 9781499316539, https://github.com/jesolem/PCV
* Hands-On Image Processing with Python, O'Reilly, ISBN: 9781789343731
