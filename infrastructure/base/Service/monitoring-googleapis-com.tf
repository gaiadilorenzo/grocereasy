resource "google_project_service" "monitoring_googleapis_com" {
  project = var.gcp_project_id
  service = "monitoring.googleapis.com"
}
# terraform import google_project_service.monitoring_googleapis_com 924197226133/monitoring.googleapis.com
