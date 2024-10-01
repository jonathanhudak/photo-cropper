# Makefile for Image Cropping App

# Variables
DOCKER_IMAGE_NAME = image_cropping_app
DOCKER_CONTAINER_NAME = image_cropping_app_container

# Default target
.PHONY: all
all: build

# Build the Docker image
.PHONY: build
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Docker container
.PHONY: run
run:
	xhost +local:docker
	docker run --rm -it \
		--name $(DOCKER_CONTAINER_NAME) \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD):/app \
		$(DOCKER_IMAGE_NAME)

# Stop the running container
.PHONY: stop
stop:
	docker stop $(DOCKER_CONTAINER_NAME)

# Remove the Docker image
.PHONY: clean
clean:
	docker rmi $(DOCKER_IMAGE_NAME)

# Show logs of the running container
.PHONY: logs
logs:
	docker logs $(DOCKER_CONTAINER_NAME)

# Enter the running container
.PHONY: shell
shell:
	docker exec -it $(DOCKER_CONTAINER_NAME) /bin/bash

# Build and run in one command
.PHONY: up
up: build run

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build  : Build the Docker image"
	@echo "  run    : Run the Docker container"
	@echo "  stop   : Stop the running container"
	@echo "  clean  : Remove the Docker image"
	@echo "  logs   : Show logs of the running container"
	@echo "  shell  : Enter the running container"
	@echo "  up     : Build and run in one command"
	@echo "  help   : Show this help message"
