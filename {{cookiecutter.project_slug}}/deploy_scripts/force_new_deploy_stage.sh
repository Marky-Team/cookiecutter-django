#!/usr/bin/bash

aws ecs update-service \
  --force-new-deployment \
  --service {{cookiecutter.project_slug}}-stage \
  --cluster stage \
  | cat && \
\
aws ecs update-service \
  --force-new-deployment \
  --service {{cookiecutter.project_slug}}-stage-celery-workers \
  --cluster stage \
  | cat
