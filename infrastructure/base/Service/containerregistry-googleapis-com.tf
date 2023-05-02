resource "google_project_service" "containerregistry_googleapis_com" {
  project = var.gcp_project_id
  service = "containerregistry.googleapis.com"
}
# terraform import google_project_service.containerregistry_googleapis_com 924197226133/containerregistry.googleapis.com
