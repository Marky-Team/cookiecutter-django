#!/usr/bin/bash

aws ecs run-task \
  --cluster stage \
  --task-definition {{cookiecutter.project_slug}}-stage-management-command \
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
