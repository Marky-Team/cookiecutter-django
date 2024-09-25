resource "aws_iam_role" "ecs-service-role" {
  name               = "${var.app_name}__${var.stage_name}__ecs_service_role"
  assume_role_policy = jsonencode({
    "Version" : "2008-10-17",
    "Statement" : [
      {
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : [
            "ecs.amazonaws.com",
            "ec2.amazonaws.com",
            "ecs-tasks.amazonaws.com"
          ]
        },
        "Effect" : "Allow"
      }
    ]
  })

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
resource "aws_iam_role_policy" "ecs-service-role-policy" {
  name   = "${var.app_name}__${var.stage_name}__ecs_service_role_policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "elasticloadbalancing:Describe*",
          "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
          "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
          "ec2:Describe*",
          "ec2:AuthorizeSecurityGroupIngress",
          "elasticloadbalancing:RegisterTargets",
          "elasticloadbalancing:DeregisterTargets"
        ],
        "Resource" : [
          "*"
        ]
      },
    ]
  })
  role = aws_iam_role.ecs-service-role.id
}
