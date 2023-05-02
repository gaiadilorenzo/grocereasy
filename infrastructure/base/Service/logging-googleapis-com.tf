resource "google_project_service" "logging_googleapis_com" {
  project = var.gcp_project_id
  service = "logging.googleapis.com"
}
# terraform import google_project_service.logging_googleapis_com 924197226133/logging.googleapis.com
