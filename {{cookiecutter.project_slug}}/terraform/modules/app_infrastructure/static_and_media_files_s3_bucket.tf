# Static and media files bucket
locals {
  s3_bucket_name = "${var.app_name}-${var.stage_name}-static-and-media-files"
}

resource "aws_s3_bucket" "static-and-media-files" {
  bucket = local.s3_bucket_name


  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }
}

resource "aws_s3_bucket_cors_configuration" "static-and-media-files" {
  bucket = aws_s3_bucket.static-and-media-files.id

  cors_rule {
    allowed_headers = [
      "Authorization"
    ]
    allowed_methods = [
      "GET"
    ]
    allowed_origins = var.cors_allowed_origins
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_policy" "static-and-media-files" {
  bucket = aws_s3_bucket.static-and-media-files.id
  policy = "${data.aws_iam_policy_document.prod_static_and_media_files.json}"

}
data "aws_iam_policy_document" "prod_static_and_media_files" {
  statement {
    sid = "PublicReadForGetBucketObjects"

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${local.s3_bucket_name}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = [
        "*"
      ]
    }
  }

  statement {
    actions = [
      "s3:*",
    ]

    resources = [
      "arn:aws:s3:::${local.s3_bucket_name}",
      "arn:aws:s3:::${local.s3_bucket_name}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = [
        aws_iam_user.s3_storage_user.arn
      ]
    }
  }
}

resource "aws_s3_bucket_public_access_block" "static-and-media-files" {
  bucket = aws_s3_bucket.static-and-media-files.id

  block_public_acls       = true
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = false
}
