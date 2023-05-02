resource "google_project_service" "storage_component_googleapis_com" {
  project = var.gcp_project_id
  service = "storage-component.googleapis.com"
}
# terraform import google_project_service.storage_component_googleapis_com 924197226133/storage-component.googleapis.com
