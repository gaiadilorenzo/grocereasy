resource "google_project_service" "cloudapis_googleapis_com" {
  project = var.gcp_project_id
  service = "cloudapis.googleapis.com"
}
# terraform import google_project_service.cloudapis_googleapis_com 924197226133/cloudapis.googleapis.com
