resource "google_project_service" "iam_googleapis_com" {
  project = var.gcp_project_id
  service = "iam.googleapis.com"
}
# terraform import google_project_service.iam_googleapis_com 924197226133/iam.googleapis.com
