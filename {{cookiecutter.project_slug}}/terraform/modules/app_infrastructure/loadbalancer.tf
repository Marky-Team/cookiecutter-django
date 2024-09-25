# Application Load Balancer
resource "aws_lb" "public_load_balancer" {
  name               = "${var.app_name}-${var.stage_name}"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [
    aws_security_group.load-balancer.id
  ]
  subnets = [for region_name, public_subnet_object in var.public_subnets : public_subnet_object.id]

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

# Target group
resource "aws_alb_target_group" "default-target-group" {
  name                 = "${var.app_name}-${var.stage_name}-tg"
  port                 = 80
  protocol             = "HTTP"
  vpc_id               = var.vpc.id
  deregistration_delay = 10

  health_check {
    path                = var.health_check_path
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 2
    interval            = 5
    matcher             = "200"
  }

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

# HTTP Listener (redirects http traffic to https)
resource "aws_alb_listener" "ecs-alb-http-listener" {
  load_balancer_arn = aws_lb.public_load_balancer.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

# HTTPS Listener (sends traffic from the load balancer to the target group)
resource "aws_alb_listener" "ecs-alb-https-listener" {
  load_balancer_arn = aws_lb.public_load_balancer.id
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate_validation.cert_validator.certificate_arn

  default_action {
    type             = "fixed-response"
    fixed_response {
      status_code = "400"
      content_type = "text/plain"
      message_body = "Invalid Host Header"
    }
  }

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_alb_listener_rule" "route_to_tg_if_host_header_matches" {
  listener_arn = aws_alb_listener.ecs-alb-https-listener.arn
  priority     = 99

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.default-target-group.arn
  }

  condition {
    host_header {
      values = var.domain_names
    }
  }
}

# ALB Security Group (Traffic Internet -> ALB)
resource "aws_security_group" "load-balancer" {
  name        = "${var.app_name}__${var.stage_name}__lb_security_group"
  description = "Controls access to the ALB for ${var.app_name}/${var.stage_name}"
  vpc_id      = var.vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
# Security Group Rule to allow access to ECS from this LB
resource "aws_security_group_rule" "example" {
  type                     = "ingress"
  protocol                 = "tcp"
  security_group_id        = var.ecs_security_group.id
  source_security_group_id = aws_security_group.load-balancer.id
  from_port                = 0
  to_port                  = 65535
}
