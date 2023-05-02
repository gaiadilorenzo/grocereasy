resource "google_project_service" "bigquerymigration_googleapis_com" {
  project = var.gcp_project_id
  service = "bigquerymigration.googleapis.com"
}
# terraform import google_project_service.bigquerymigration_googleapis_com 924197226133/bigquerymigration.googleapis.com
