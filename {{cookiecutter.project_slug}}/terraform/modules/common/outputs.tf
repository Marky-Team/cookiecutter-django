output "bastion_sg" {
  value = data.aws_security_group.bastion_sg
}

output "ecs_stage_sg" {
  value = data.aws_security_group.ecs_stage_sg
}

output "ecs_prod_sg" {
  value = data.aws_security_group.ecs_prod_sg
}

output "prod_ecs_cluster" {
  value = data.aws_ecs_cluster.prod
}

output "private_subnets" {
  value = data.aws_subnet.private_subnets
}

output "public_subnets" {
  value = data.aws_subnet.public_subnets
}

output "repo" {
  value = data.aws_ecr_repository.repo
}

output "stage_ecs_cluster" {
  value = data.aws_ecs_cluster.stage
}

output "vpc" {
  value = data.aws_vpc.vpc
}
