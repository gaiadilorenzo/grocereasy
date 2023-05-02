resource "google_project_service" "compute_googleapis_com" {
  project = var.gcp_project_id
  service = "compute.googleapis.com"
}
# terraform import google_project_service.compute_googleapis_com 924197226133/compute.googleapis.com
