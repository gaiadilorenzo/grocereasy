resource "google_project_service" "servicemanagement_googleapis_com" {
  project = var.gcp_project_id
  service = "servicemanagement.googleapis.com"
}
# terraform import google_project_service.servicemanagement_googleapis_com 924197226133/servicemanagement.googleapis.com
