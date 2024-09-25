resource "aws_iam_role" "ecs_task_start_role" {
  name               = "${var.app_name}__${var.stage_name}__ecs_task_start_role"
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

locals {
  ecs_task_role_policy = {
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "secretsmanager:GetSecretValue"
        ],
        "Effect" : "Allow",
        "Resource" : concat(
          [
            aws_secretsmanager_secret.database_password_secret.arn,
            aws_secretsmanager_secret.s3_access_key_id.arn,
            aws_secretsmanager_secret.s3_secret_access_key.arn,
            aws_secretsmanager_secret.ses_access_key_id.arn,
            aws_secretsmanager_secret.ses_secret_access_key.arn,
            aws_secretsmanager_secret.django_secret_key.arn,
          ],
          [
            for k, v in aws_secretsmanager_secret.extra_secrets : v.arn
          ],
        )
      },
      {
        "Sid" : "ListImagesInRepository",
        "Effect" : "Allow",
        "Action" : [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ],
        "Resource" : "arn:aws:ecr:${var.aws_region}:${var.aws_account_id}:repository/${var.image_repository.name}"
      },
      {
        "Sid" : "GetAuthorizationToken",
        "Effect" : "Allow",
        "Action" : [
          "ecr:GetAuthorizationToken",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      },
    ]
  }
}

resource "aws_iam_role_policy" "ecs-task-role-policy" {
  name   = "${var.app_name}__${var.stage_name}__ecs_task_role_policy"
  policy = jsonencode(local.ecs_task_role_policy)
  role   = aws_iam_role.ecs_task_start_role.id
}


resource "aws_iam_role" "ecs_task_role" {
  name               = "${var.app_name}__${var.stage_name}__ecs_task_role"
  description        = <<-END_OF_DESCRIPTION
      This role allows ECS tasks to access necessary resources for the ${var.app_name} application in the
      ${var.stage_name} environment. This is only used by the task executiable itself to make calls to AWS services
      (typically things like S3, Dynamo, etc.).
      END_OF_DESCRIPTION
  assume_role_policy = jsonencode({
    "Version" : "2008-10-17",
    "Statement" : [
      {
        "Effect" : "Allow"
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : [
            "ecs-tasks.amazonaws.com"
          ]
        }
      }
    ]
  })

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_iam_role_policy_attachment" "task_role_access" {
  policy_arn = aws_iam_policy.task_role_policy.arn
  role       = aws_iam_role.ecs_task_role.name
}

resource "aws_iam_policy" "task_role_policy" {
  name   = "${var.app_name}_${var.stage_name}__ecs_task_role_policy"
  policy = data.aws_iam_policy_document.task_role_access.json
}

data "aws_iam_policy_document" "task_role_access" {
  statement {
    sid     = "SESAccess"
    actions = [
      "ses:*",
    ]
    resources = [
      "*",
    ]
  }
}
