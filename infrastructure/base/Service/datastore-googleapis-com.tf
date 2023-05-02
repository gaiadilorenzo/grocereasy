resource "google_project_service" "datastore_googleapis_com" {
  project = var.gcp_project_id
  service = "datastore.googleapis.com"
}
# terraform import google_project_service.datastore_googleapis_com 924197226133/datastore.googleapis.com
