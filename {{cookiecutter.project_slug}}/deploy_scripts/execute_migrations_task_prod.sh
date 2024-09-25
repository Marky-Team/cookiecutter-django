#!/usr/bin/bash

aws ecs run-task \
  --cluster prod \
  --task-definition {{cookiecutter.project_slug}}-prod-management-command \
  --overrides '
  {
    "containerOverrides":[
      {
        "name":"django-app",
        "command":["python3", "manage.py", "migrate", "--no-input"]
      }
    ]
  }' \
  | cat
