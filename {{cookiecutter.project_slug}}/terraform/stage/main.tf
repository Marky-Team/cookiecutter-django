module "common" {
  source = "../modules/common"
}

module "stage" {
  source               = "../modules/app_infrastructure"
  aws_region           = "us-east-1"
  app_name             = "{{cookiecutter.project_slug}}"
  stage_name           = "stage"
  bastion_sg           = module.common.bastion_sg
  domain_names         = ["stage.{{cookiecutter.domain_name}}"]
  ecs_cluster          = module.common.stage_ecs_cluster
  ecs_security_group   = module.common.ecs_stage_sg
  image_repository     = module.common.repo
  private_subnets      = module.common.private_subnets
  public_subnets       = module.common.public_subnets
  vpc                  = module.common.vpc
  cors_allowed_origins = [
    "https://stage.{{cookiecutter.domain_name}}",
  ]
  additional_env_vars = {
    SES_EMAIL_ENABLED : "False"
    DJANGO_DEBUG : "True"
    AWS_DEFAULT_REGION : "us-east-1"
    DJANGO_ACCOUNT_ALLOW_REGISTRATION : "False",
    DJANGO_ADMIN_URL : "admin/",
    DJANGO_ALLOWED_HOSTS : "stage.{{cookiecutter.domain_name}}"
    DJANGO_SETTINGS_MODULE : "config.settings.combined",
    DJANGO_SECURE_SSL_REDIRECT : "True",
  }
  env_secret_names = {
  }
}
