resource "google_project_service" "bigquerystorage_googleapis_com" {
  project = var.gcp_project_id
  service = "bigquerystorage.googleapis.com"
}
# terraform import google_project_service.bigquerystorage_googleapis_com 924197226133/bigquerystorage.googleapis.com
