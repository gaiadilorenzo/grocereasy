resource "google_project_service" "cloudtrace_googleapis_com" {
  project = var.gcp_project_id
  service = "cloudtrace.googleapis.com"
}
# terraform import google_project_service.cloudtrace_googleapis_com 924197226133/cloudtrace.googleapis.com
