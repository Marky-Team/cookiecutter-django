#!/usr/bin/bash

aws ecs run-task \
  --cluster stage \
  --task-definition {{cookiecutter.project_slug}}-stage-management-command \
  --overrides '
  {
    "containerOverrides":[
      {
        "name":"django-app",
        "command":[
          "python3",
          "manage.py",
          "createsuperuser",
          "--no-input",
          "--username", "USERNAME_REPLACE_ME!",
          "--email", "YOUR@EMAIL.HERE"
        ]
      }
    ]
  }' \
  | cat
