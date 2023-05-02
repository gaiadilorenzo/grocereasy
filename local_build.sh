#!/bin/bash


# Build docker images and push to Docker Hub repository.
for component in orchestrator worker storer
do
  echo $component
  docker build -t $component --build-arg COMPONENT=$component  .
done
