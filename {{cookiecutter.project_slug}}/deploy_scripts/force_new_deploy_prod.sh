#!/usr/bin/bash

aws ecs update-service \
  --force-new-deployment \
  --service {{cookiecutter.project_slug}}-prod \
  --cluster prod \
  | cat && \
\
aws ecs update-service \
  --force-new-deployment \
  --service {{cookiecutter.project_slug}}-prod-celery-workers \
  --cluster prod \
  | cat
