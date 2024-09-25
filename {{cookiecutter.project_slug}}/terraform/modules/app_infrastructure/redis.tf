resource "aws_elasticache_cluster" "example" {
  cluster_id           = "${var.app_name}-${var.stage_name}"
  engine               = "redis"
  node_type            = "cache.m4.large"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.1"
  port                 = 6379

  security_group_ids = [aws_security_group.redis_security_group.id]
}

resource "aws_security_group" "redis_security_group" {
  name = "${var.app_name}-${var.stage_name}"
  ingress {
    description     = "Access from ECS"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.ecs_security_group.id]
  }
  egress {
    description     = "Access to ECS"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.ecs_security_group.id]
  }
  ingress {
    description     = "Access from Bastion"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.bastion_sg.id]
  }
  egress {
    description     = "Access to ECS"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [var.bastion_sg.id]
  }
}
