## Local Development

### Run Tests
```bash
docker compose up test
```

#### Run a single test
Here is an example command for running a single test:
`docker compose run test python manage.py test --keepdb {app_name}.tests.{file_name}.{class}.{test}`
eg
`docker compose run test python manage.py test --keepdb post_generator.tests.test_generate_caption_view.GenerateCaptionViewTests.test_generate_caption_success`


#### Handling Test Database Persistence in Docker (Django)

When running docker compose up test, you may encounter the following error:
```
EOFError: EOF when reading a line
Type 'yes' if you would like to try deleting the test database 'test_marky_django', or 'no' to cancel:
```

This happens when Django’s test runner crashes before properly cleaning up the test database. To avoid this, you can:
- Run tests with: `docker compose run --rm test python manage.py test --no-input`
- (Recommended) Use the --keepdb flag for faster test runs and to avoid recreation every time: `docker compose run --rm test python manage.py test --keepdb`
- If you hit inconsistent migrations (due to removed migrations), rerun without `--keepdb` and type “yes” when prompted.


### Managing Secrets
Secrets (like API Keys) are stored in aws secrets manager and retrieved through terraform.
1. Add the secret name to `env_secret_names` mapping in the `terraform/prod/main.tf` (and stage) files.
2. Apply the terraform (See `Terraform` section)
3. Navigate to [secretsmanager](https://us-east-1.console.aws.amazon.com/secretsmanager/listsecrets?region=us-east-1) and click "Store a new secret"

### Terraform
```bash
brew install terraform # (brew for mac). can't use docker for terraform
cd terraform/stage # (or prod)
terraform init
terraform plan # (optionally send that plan to someone for validation)
terraform apply
```

## Contributing
### Using pre-commit when committing code
Before you begin, you should install [pre-commit](https://pre-commit.com/):
```bash
pip install pre-commit
```
And install the precommit hooks:
```bash
pre-commit install
```
This will automatically run all checks on commit, if you need to run the formatter and
checks without commiting, you can use this:
```bash
pre-commit run
```

## Deployment
Deployment is managed via CICD (github actions) when the a commit is made to `staging` or `prod` branches


## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.
