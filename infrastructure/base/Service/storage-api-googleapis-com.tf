resource "google_project_service" "storage_api_googleapis_com" {
  project = var.gcp_project_id
  service = "storage-api.googleapis.com"
}
# terraform import google_project_service.storage_api_googleapis_com 924197226133/storage-api.googleapis.com
