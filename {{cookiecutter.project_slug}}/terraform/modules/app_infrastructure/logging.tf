# Logging config
resource "aws_cloudwatch_log_group" "log-group" {
  name              = "/ecs/${var.app_name}/${var.stage_name}"
  retention_in_days = var.log_retention_in_days

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
