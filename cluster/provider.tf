provider "google" {
  credentials = "auth/svc.json"
  project     = "<your-gcp-project>"
  region      = "europe-west2"
}

provider "kubernetes" {
  load_config_file       = false
  host                   = "https://${module.cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}
