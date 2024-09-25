# SSL Certificate
resource "aws_acm_certificate" "cert" {
  domain_name               = var.domain_names[0]
  subject_alternative_names = var.domain_names
  validation_method         = "DNS"

  tags = {
    Environment = var.stage_name
    Application = var.app_name
  }

  lifecycle {
    create_before_destroy = true
  }
}
locals {
  domain_name_to_zone_id_map = {
    for idx, domain_name in var.domain_names : domain_name => data.aws_route53_zone.top_level_zones[idx].zone_id
  }
}
resource "aws_route53_record" "ssl_cert_validation_records" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [
    each.value.record
  ]
  ttl     = 60
  type    = each.value.type
  zone_id = local.domain_name_to_zone_id_map[each.key]
}
resource "aws_acm_certificate_validation" "cert_validator" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.ssl_cert_validation_records : record.fqdn]
}
