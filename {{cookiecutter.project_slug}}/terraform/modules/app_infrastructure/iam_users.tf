resource "aws_iam_user" "s3_storage_user" {
  name = "${var.app_name}_${var.stage_name}__s3_storage_user"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}
