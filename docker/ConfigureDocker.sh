#!/bin/bash
# Create the docker "image"; this is the tempate that containers are created from.
# Both images are tagged with pipetag; this will help prevent multiple overlapping instances from running.
# This file should create both images

# CLI
# Dockerfile is located in subdirectory dockerfiles\cli

docker build -t cli \
	./CLI/

# GUI
# Dockerfile is located in subdirectory dockerfiles\gui
docker build -t gui \
	./GUI/
