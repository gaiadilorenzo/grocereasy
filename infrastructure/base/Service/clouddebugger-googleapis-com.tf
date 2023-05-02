resource "google_project_service" "clouddebugger_googleapis_com" {
  project = var.gcp_project_id
  service = "clouddebugger.googleapis.com"
}
# terraform import google_project_service.clouddebugger_googleapis_com 924197226133/clouddebugger.googleapis.com
