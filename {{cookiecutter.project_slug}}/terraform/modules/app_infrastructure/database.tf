resource "aws_db_instance" "db" {
  identifier             = "${var.app_name}-${var.stage_name}"
  db_name                = "${replace(var.app_name, "-", "_")}_${var.stage_name}"
  username               = "rds_admin"
  password               = aws_secretsmanager_secret_version.database_password_secret_version.secret_string
  port                   = "5432"
  engine                 = "postgres"
  engine_version         = "16.2"
  instance_class         = var.rds_instance_class
  allocated_storage      = "20"
  storage_encrypted      = false
  vpc_security_group_ids = [
    aws_security_group.rds.id
  ]
  db_subnet_group_name    = aws_db_subnet_group.db-subnet.name
  multi_az                = var.db_multi_az
  storage_type            = "gp2"
  publicly_accessible     = false
  backup_retention_period = 7
  skip_final_snapshot     = true

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
  lifecycle {
    ignore_changes = [
      engine_version
    ]
  }
}

resource "aws_db_subnet_group" "db-subnet" {
  name       = "${var.app_name}-${var.stage_name}"
  subnet_ids = [for region_name, public_subnet_object in var.private_subnets : public_subnet_object.id]

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_security_group" "rds" {
  name        = "${var.app_name}-${var.stage_name}-rds-security-group"
  description = "Allows inbound access from ECS only"
  vpc_id      = var.vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = "5432"
    to_port         = "5432"
    security_groups = [
      var.ecs_security_group.id,
      var.bastion_sg.id
    ]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
