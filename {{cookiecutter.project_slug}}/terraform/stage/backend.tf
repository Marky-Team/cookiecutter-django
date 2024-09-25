terraform {
  backend "s3" {
    bucket         = "marky-terraform-state"
    key            = "terraform/state/{{cookiecutter.project_slug}}/stage"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"
  }
}
