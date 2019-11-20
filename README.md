# Detect Scratches
Experiments into the field of computer vision.

## used libaries
* numpy
* matplotlib
* Pillow
* scipy

see docker/requirements-full.txt for the full list


## Docker deployment
Clone the repository using
`git clone https://github.com/felixschloesser/DetectScratches.git`

Enter the directory: `cd DetectScratches/docker`

All you have to do is adjust binding path inside the docker-compose.yml to your cloned notebook folder.

Docker will take care of the rest for you :)
`docker-compose up`
Now you can navigate to http://127.0.0.1/:8888 to access the jupyter notebook.

Have fun!
