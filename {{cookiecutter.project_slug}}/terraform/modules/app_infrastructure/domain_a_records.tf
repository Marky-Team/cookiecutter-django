data "aws_route53_zone" "top_level_zones" {
  count = length(var.domain_names)

  name         = "${join(".", reverse(slice(reverse(split(".", var.domain_names[count.index])), 0, 2)))}."
  private_zone = false
}


# Route53 Records
resource "aws_route53_record" "domain_a_records" {
  count = length(var.domain_names)

  zone_id = data.aws_route53_zone.top_level_zones[count.index].zone_id
  name    = var.domain_names[count.index]
  type    = "A"

  alias {
    evaluate_target_health = false
    name                   = aws_lb.public_load_balancer.dns_name
    zone_id                = aws_lb.public_load_balancer.zone_id
  }
}
