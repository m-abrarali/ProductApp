terraform {
  backend "gcs" {
    bucket      = "<your-bucket-name>"
    prefix      = "gke-cluster/terraform-state.tfstate"
    credentials = "./auth/svc.json"
  }
}
