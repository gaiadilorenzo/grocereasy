resource "google_project_service" "serviceusage_googleapis_com" {
  project = var.gcp_project_id
  service = "serviceusage.googleapis.com"
}
# terraform import google_project_service.serviceusage_googleapis_com 924197226133/serviceusage.googleapis.com
