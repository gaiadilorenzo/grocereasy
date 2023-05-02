resource "google_project_service" "cloudasset_googleapis_com" {
  project = var.gcp_project_id
  service = "cloudasset.googleapis.com"
}
# terraform import google_project_service.cloudasset_googleapis_com 924197226133/cloudasset.googleapis.com
