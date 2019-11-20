# Detect Scratches
Experiments into the field of computer vision done at my three month internship at Rongheng Information Technology Co. Ltd. in Shanghai.

## Used Libraries
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
