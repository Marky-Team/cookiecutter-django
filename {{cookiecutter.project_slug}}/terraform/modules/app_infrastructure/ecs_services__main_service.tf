# ECS Service
resource "aws_ecs_service" "service" {
  name            = "${var.app_name}-${var.stage_name}"
  cluster         = var.ecs_cluster.id
  task_definition = aws_ecs_task_definition.app.arn
  iam_role        = aws_iam_role.ecs-service-role.arn
  desired_count   = var.app_count
  depends_on      = [
    aws_alb_listener.ecs-alb-http-listener,
    aws_iam_role_policy.ecs-service-role-policy
  ]
  health_check_grace_period_seconds = 60


  load_balancer {
    target_group_arn = aws_alb_target_group.default-target-group.arn
    container_name   = "django-app"
    container_port   = 80
  }

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
