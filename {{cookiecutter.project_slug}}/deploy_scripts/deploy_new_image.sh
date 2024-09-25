#!/usr/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 679808196654.dkr.ecr.us-east-1.amazonaws.com && \
\
docker-compose build django && \
\
docker tag {{cookiecutter.python_package_name}}_local_django 679808196654.dkr.ecr.us-east-1.amazonaws.com/{{cookiecutter.project_slug}}:latest && \
docker push 679808196654.dkr.ecr.us-east-1.amazonaws.com/{{cookiecutter.project_slug}}:latest
# TODO: Figure out how to make this not rely on "latest" build
