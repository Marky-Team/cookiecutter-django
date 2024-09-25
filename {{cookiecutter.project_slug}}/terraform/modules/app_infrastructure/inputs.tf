variable "additional_env_vars" {
  type = map(string)
}

variable "app_count" {
  type    = number
  default = 2
}

variable "app_name" {
  type = string
}

variable "aws_account_id" {
  type    = string
  default = "679808196654"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "bastion_sg" {
  type = object({
    id : string
  })
}

variable "celery_worker_count" {
  type    = number
  default = 2
}

variable "celery_worker_cpu_reservation" {
  type    = number
  default = 10
}

variable "celery_worker_memory_limit_mb" {
  type    = number
  default = 1024
}

variable "celery_worker_memory_reservation_mb" {
  type    = number
  default = 128
}

variable "cors_allowed_origins" {
  type = set(string)
}

variable "db_multi_az" {
  default = true
  type    = bool
}

variable "domain_names" {
  type = list(string)
}

variable "env_secret_names" {
  type = map(string)
}

variable "ecs_cluster" {
  type = object({
    id : string
  })
}

variable "ecs_security_group" {
  type = object({
    id : string
  })
}

variable "health_check_path" {
  default = "/health-check"
}

variable "image_repository" {
  type = object({
    name : string,
    repository_url : string
  })
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "log_retention_in_days" {
  default = 30
  type    = number
}

variable "public_subnets" {
  type = map(object({
    id : string
  }))
}

variable "private_subnets" {
  type = map(object({
    id : string
  }))
}

variable "rds_instance_class" {
  default = "db.t4g.micro"
}

variable "sentry_environment_name_override" {
  # DO NOT USE THIS AS THE VALUE; USE `locals.sentry_environment_name` instead which provides a default value
  type = string
  default = null
}

locals {
  sentry_environment_name = coalesce(var.sentry_environment_name_override, var.stage_name)
}

variable "stage_name" {
  type = string
}

variable "vpc" {
  type = object({
    id : string
  })
}
