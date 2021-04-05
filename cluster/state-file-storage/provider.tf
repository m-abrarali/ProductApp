terraform {
  required_version = ">= 0.13"
}
provider "google" {
  credentials = file(var.gcp_auth_file)
  project     = var.gcp_project
  region      = var.gcp_region
}
