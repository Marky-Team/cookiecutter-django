module "common" {
  source = "../modules/common"
}

module "prod" {
  source              = "../modules/app_infrastructure"
  aws_region          = "us-east-1"
  app_name            = "{{cookiecutter.project_slug}}"
  stage_name          = "prod"
  bastion_sg          = module.common.bastion_sg
  domain_names        = ["{{cookiecutter.domain_name}}"]
  ecs_cluster         = module.common.prod_ecs_cluster
  ecs_security_group  = module.common.ecs_prod_sg
  image_repository    = module.common.repo
  private_subnets     = module.common.private_subnets
  public_subnets      = module.common.public_subnets
  vpc                 = module.common.vpc
  additional_env_vars = {
    SES_EMAIL_ENABLED : "False"
    DJANGO_DEBUG : "False"
    AWS_DEFAULT_REGION : "us-east-1"
    DJANGO_ACCOUNT_ALLOW_REGISTRATION : "False",
    DJANGO_ADMIN_URL : "admin/",
    DJANGO_ALLOWED_HOSTS : "backend.mymarky.net"
    DJANGO_SETTINGS_MODULE : "config.settings.combined",
    DJANGO_SECURE_SSL_REDIRECT : "True",
    MEDIA_SERVICE_BASE_URL : "https://{{cookiecutter.domain_name}}",
    CONN_MAX_AGE : "0"
  }
  env_secret_names = {
  }
  cors_allowed_origins = [
    "https://{{cookiecutter.domain_name}}",
  ]
  sentry_environment_name_override = "production"
  celery_worker_cpu_reservation = 256
  celery_worker_memory_reservation_mb = 256
  celery_worker_memory_limit_mb = 4096
}
