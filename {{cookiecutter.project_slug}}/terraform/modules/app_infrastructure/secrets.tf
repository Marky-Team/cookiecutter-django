resource "random_password" "database_password" {
  length  = 16
  special = false
}

resource "aws_secretsmanager_secret" "database_password_secret" {
  name = "/${var.app_name}/${var.stage_name}/database/password/primary"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_secretsmanager_secret_version" "database_password_secret_version" {
  secret_id     = aws_secretsmanager_secret.database_password_secret.id
  secret_string = random_password.database_password.result
}


resource "aws_iam_access_key" "s3_storage_user" {
  user = aws_iam_user.s3_storage_user.name
}
resource "aws_secretsmanager_secret" "s3_access_key_id" {
  name = "/${var.app_name}/${var.stage_name}/s3_user/access_key_id"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
resource "aws_secretsmanager_secret_version" "s3_access_key_id_arn_version" {
  secret_id     = aws_secretsmanager_secret.s3_access_key_id.id
  secret_string = aws_iam_access_key.s3_storage_user.id
}
resource "aws_secretsmanager_secret" "s3_secret_access_key" {
  name = "/${var.app_name}/${var.stage_name}/s3_user/secret_access_key"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
resource "aws_secretsmanager_secret_version" "s3_secret_access_key_version" {
  secret_id     = aws_secretsmanager_secret.s3_secret_access_key.id
  secret_string = aws_iam_access_key.s3_storage_user.secret
}


resource "aws_iam_access_key" "ses_user" {
  user = aws_iam_user.ses_user.name
}
resource "aws_secretsmanager_secret" "ses_access_key_id" {
  name = "/${var.app_name}/${var.stage_name}/ses_user/access_key_id"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
resource "aws_secretsmanager_secret_version" "ses_access_key_id_version" {
  secret_id     = aws_secretsmanager_secret.ses_access_key_id.id
  secret_string = aws_iam_access_key.ses_user.id
}
resource "aws_secretsmanager_secret" "ses_secret_access_key" {
  name = "/${var.app_name}/${var.stage_name}/ses_user/secret_access_key"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
resource "aws_secretsmanager_secret_version" "ses_secret_access_key_version" {
  secret_id     = aws_secretsmanager_secret.ses_secret_access_key.id
  secret_string = aws_iam_access_key.ses_user.secret
}


resource "random_password" "django_secret_key" {
  length = 50
}

resource "aws_secretsmanager_secret" "django_secret_key" {
  name = "/${var.app_name}/${var.stage_name}/django_secret_key"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_secretsmanager_secret_version" "django_secret_key_version" {
  secret_id     = aws_secretsmanager_secret.django_secret_key.id
  secret_string = random_password.django_secret_key.result
}


resource "aws_secretsmanager_secret" "extra_secrets" {
  for_each = var.env_secret_names
  name = "/${var.app_name}/${var.stage_name}/extra/${each.value}"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
