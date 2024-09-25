resource "aws_ecr_repository" "marky-backend-repo" {
  name                 = "{{cookiecutter.project_slug}}"
  image_tag_mutability = "MUTABLE"
}
