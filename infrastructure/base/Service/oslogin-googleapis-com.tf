resource "google_project_service" "oslogin_googleapis_com" {
  project = var.gcp_project_id
  service = "oslogin.googleapis.com"
}
# terraform import google_project_service.oslogin_googleapis_com 924197226133/oslogin.googleapis.com
