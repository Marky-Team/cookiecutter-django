locals {
  management_task_template = merge(
    local.service_task_template,
    {
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : "/ecs/${var.app_name}/${var.stage_name}",
          "awslogs-region" : var.aws_region,
          "awslogs-stream-prefix" : "management-command",
        }
      }
    })
}

resource "aws_ecs_task_definition" "management-command" {
  family                = "${var.app_name}-${var.stage_name}-management-command"
  container_definitions = jsonencode([local.management_task_template])
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
