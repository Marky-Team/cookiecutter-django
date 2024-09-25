# ECS Service
resource "aws_ecs_service" "celery_workers" {
  name            = "${var.app_name}-${var.stage_name}-celery-workers"
  cluster         = var.ecs_cluster.id
  task_definition = aws_ecs_task_definition.celery-wokers.arn
  desired_count   = var.celery_worker_count

  lifecycle {
    ignore_changes = [
      capacity_provider_strategy,
      deployment_circuit_breaker,
      deployment_controller
    ]
  }

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
