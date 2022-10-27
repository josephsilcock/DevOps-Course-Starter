variable "github_client_id" {
  description = "Github OAuth Client ID"
  sensitive   = true
}

variable "github_client_secret" {
  description = "Github OAuth Client ID"
  sensitive   = true
}

variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "secret_key" {
  description = "Flask secret key"
  sensitive   = true
}

variable "loggly_token" {
  description = "Loggly token"
  sensitive   = true
}