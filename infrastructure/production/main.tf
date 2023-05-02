module "root" {
  source = "../base"

  gcp_project_id = var.gcp_project_id
  gcp_zone = var.gcp_zone

}