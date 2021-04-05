module "network" {
  source = "git@github.com:FairwindsOps/terraform-gcp-vpc-native.git//default?ref=default-v2.2.2"
  // base network parameters
  network_name    = "kube"
  subnetwork_name = "kube-subnet"
  region          = var.gcp_region
  // subnetwork primary and secondary CIDRS for IP aliasing
  subnetwork_range    = "10.40.0.0/16"
  subnetwork_pods     = "10.41.0.0/16"
  subnetwork_services = "10.42.0.0/16"
}

module "cluster" {
  source                           = "git@github.com:FairwindsOps/terraform-gke.git//vpc-native?ref=vpc-native-v1.4.1"
  region                           = var.gcp_region
  name                             = "gke-cluster"
  project                          = var.gcp_project
  network_name                     = "kube"
  nodes_subnetwork_name            = module.network.subnetwork
  kubernetes_version               = "1.18.16-gke.302"
  pods_secondary_ip_range_name     = module.network.gke_pods_1
  services_secondary_ip_range_name = module.network.gke_services_1
}

module "node_pool" {
  source             = "git@github.com:/FairwindsOps/terraform-gke//node_pool?ref=node-pool-v3.3.0"
  name               = "gke-cluster-node-pool"
  region             = module.cluster.region
  gke_cluster_name   = module.cluster.name
  machine_type       = "n1-standard-4"
  min_node_count     = "1"
  max_node_count     = "2"
  kubernetes_version = module.cluster.kubernetes_version
}
