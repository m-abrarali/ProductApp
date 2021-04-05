# define GCP region
variable "gcp_region" {
  type        = string
  description = "GCP region"
  default     = "europe-west2"
}

# define GCP project name
variable "gcp_project" {
  type        = string
  description = "GCP project name"
}

# GCP authentication file
variable "gcp_auth_file" {
  type        = string
  description = "GCP authentication file"
  default     = "auth/svc.json"
}
