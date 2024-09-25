# ECS Task Definition
locals {
  service_task_template = {
    "name" : "django-app",
    "image" : "${var.image_repository.repository_url}:${var.image_tag}",
    "essential" : true,
    "cpu" : 10,
    "memory" : 950,
    "memoryReservation" : 256,
    "links" : [],
    "portMappings" : [
      {
        "containerPort" : 80,
        "hostPort" : 0,
        "protocol" : "tcp"
      }
    ],
    "command" : [
      "gunicorn",
      "-w", "3",
      "-b", ":80",
      "config.wsgi:application"
    ],
    "environment" : concat(
      [
        {
          name : "POSTGRES_HOST",
          value : aws_db_instance.db.address,
        },
        {
          name : "POSTGRES_DB",
          value : aws_db_instance.db.db_name,
        },
        {
          name : "POSTGRES_PORT",
          value : tostring(aws_db_instance.db.port),
        },
        {
          name : "POSTGRES_USER",
          value : aws_db_instance.db.username,
        },
        {
          name : "DJANGO_AWS_STORAGE_BUCKET_NAME",
          value : aws_s3_bucket.static-and-media-files.bucket,
        },
        {
          name : "REDIS_URL",
          value : "redis://${aws_elasticache_cluster.example.cluster_id}.ef6vop.0001.use1.cache.amazonaws.com:${aws_elasticache_cluster.example.port}/0"
        },
        {
          name : "CORS_ALLOWED_ORIGINS",
          value : join(",", var.cors_allowed_origins)
        },
        {
          name : "DYNAMO_DB_TABLE_POSTFIX",
          value : var.dynamo_db_table_postfix,
        },
        {
          name : "SENTRY_ENVIRONMENT",
          value : local.sentry_environment_name,
        },
      ],
      [
        for env_name, value in var.additional_env_vars :
        {
          name : env_name,
          value : value,
        }
      ]
    ),
    "secrets" : concat(
      [
        {
          name : "AWS_SES_ACCESS_KEY_ID",
          valueFrom : aws_secretsmanager_secret.ses_access_key_id.arn,
        },
        {
          name : "AWS_SES_SECRET_ACCESS_KEY",
          valueFrom : aws_secretsmanager_secret.ses_secret_access_key.arn,
        },
        {
          name : "DJANGO_AWS_ACCESS_KEY_ID",
          valueFrom : aws_secretsmanager_secret.s3_access_key_id.arn,
        },
        {
          name : "DJANGO_AWS_SECRET_ACCESS_KEY",
          valueFrom : aws_secretsmanager_secret.s3_secret_access_key.arn,
        },
        {
          name : "DJANGO_SECRET_KEY",
          valueFrom : aws_secretsmanager_secret.django_secret_key.arn,
        },
        {
          name : "POSTGRES_PASSWORD",
          valueFrom : aws_secretsmanager_secret.database_password_secret.arn,
        },
      ],
      [
        for k, v in aws_secretsmanager_secret.extra_secrets :
        {
          name : upper(k),
          valueFrom : v.arn,
        }
      ]
    ),
    "logConfiguration" : {
      "logDriver" : "awslogs",
      "options" : {
        "awslogs-group" : "/ecs/${var.app_name}/${var.stage_name}",
        "awslogs-region" : var.aws_region,
        "awslogs-stream-prefix" : "app",
      }
    },
    "linuxParameters": {
      "initProcessEnabled": true,
    }
  }
}

resource "aws_ecs_task_definition" "app" {
  family                = "${var.app_name}-${var.stage_name}"
  container_definitions = jsonencode([local.service_task_template])
  depends_on            = [
    aws_db_instance.db
  ]
  execution_role_arn = aws_iam_role.ecs_task_start_role.arn
  task_role_arn = aws_iam_role.ecs_task_role.arn

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
