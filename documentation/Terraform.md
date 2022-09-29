# Terraform

We use terraform to manage our cloud infrastructure. You will need to create a `terraform.tfvars` file using the
template provided, then run:
```bash
terraform init
```
to set it up.

In the deployment stage of the CI/CD pipeline, `terraform apply` is run, to deploy the updated code.