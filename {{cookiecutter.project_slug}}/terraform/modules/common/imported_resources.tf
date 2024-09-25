data "aws_ecr_repository" "repo" {
  name = "{{cookiecutter.project_slug}}"
}

data "aws_ecs_cluster" "prod" {
  cluster_name = "prod"
}
data "aws_ecs_cluster" "stage" {
  cluster_name = "stage"
}

data "aws_security_group" "bastion_sg" {
  id = "sg-0f9971f755ab80425"
}

data "aws_security_group" "ecs_stage_sg" {
  id = "sg-0f0787166b57a0f5e"
}

data "aws_security_group" "ecs_prod_sg" {
  id = "sg-023cea90e08889ca3"
}

data "aws_subnet" "public_subnets" {
  for_each = toset([
    "subnet-0513576cca35f9a49",
    "subnet-05ada5d1d0f39fb00",
    "subnet-04745fed35706cb71",
    "subnet-033b955dcde819331",
    "subnet-028072a57684d3ea8",
    "subnet-0ae995812f4863feb",
  ])
  id = each.value
}

data "aws_subnet" "private_subnets" {
  for_each = toset([
    "subnet-0c64a53146b9b8f67",
    "subnet-031e8b931bb0a1f09",
    "subnet-049aab21d7b2f0ae1",
    "subnet-0e962b77188071df5",
    "subnet-0face23c6b1f6e9af",
    "subnet-066feae8ae161277a",
  ])
  id = each.value
}

data "aws_vpc" "vpc" {
  id = "vpc-017a8451dca88cda7"
}
