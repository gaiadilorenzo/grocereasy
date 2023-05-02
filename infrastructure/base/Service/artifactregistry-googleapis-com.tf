resource "google_project_service" "artifactregistry_googleapis_com" {
  project = var.gcp_project_id
  service = "artifactregistry.googleapis.com"
}
# terraform import google_project_service.artifactregistry_googleapis_com 924197226133/artifactregistry.googleapis.com
