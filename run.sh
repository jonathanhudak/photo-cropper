#!/bin/bash
xhost +local:docker
docker run --rm -it     -e DISPLAY=$DISPLAY     -v /tmp/.X11-unix:/tmp/.X11-unix     -v $(pwd):/app     image_cropping_app
