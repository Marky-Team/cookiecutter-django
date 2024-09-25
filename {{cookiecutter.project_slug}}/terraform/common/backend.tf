terraform {
  backend "s3" {
    bucket         = "marky-terraform-state"
    key            = "terraform/state/{{cookiecutter.project_slug}}/common"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}
