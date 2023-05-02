resource "google_project_service" "iamcredentials_googleapis_com" {
  project = var.gcp_project_id
  service = "iamcredentials.googleapis.com"
}
# terraform import google_project_service.iamcredentials_googleapis_com 924197226133/iamcredentials.googleapis.com
