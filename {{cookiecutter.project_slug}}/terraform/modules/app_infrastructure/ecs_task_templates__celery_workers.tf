locals {
  celery_workers_task_template = merge(
    local.service_task_template,
    {
      "cpu" : var.celery_worker_cpu_reservation,
      "memory" : var.celery_worker_memory_limit_mb,
      "memoryReservation" : var.celery_worker_memory_reservation_mb,
      "portMappings" : [],
      "command" : [
        "celery",
        "-A", "config.celery_app",
        "worker",
        "-l", "info",
      ],
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : "/ecs/${var.app_name}/${var.stage_name}",
          "awslogs-region" : var.aws_region,
          "awslogs-stream-prefix" : "celery-workers",
        }
      }
    })
}

resource "aws_ecs_task_definition" "celery-wokers" {
  family                = "${var.app_name}-${var.stage_name}-celery-wokers"
  container_definitions = jsonencode([local.celery_workers_task_template])
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
