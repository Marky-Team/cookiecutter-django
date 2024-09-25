resource "aws_iam_user" "ses_user" {
  name = "${var.app_name}_${var.stage_name}__ses_user"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_iam_policy" "ses_access" {
  policy = data.aws_iam_policy_document.ses_access.json

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_iam_user_policy_attachment" "ses_user" {
  policy_arn = aws_iam_policy.ses_access.arn
  user       = aws_iam_user.ses_user.name
}

data "aws_iam_policy_document" "ses_access" {
  statement {
    sid = "SESAccess"

    actions = [
      "ses:*",
    ]

    resources = [
      "*",
    ]

  }
}
