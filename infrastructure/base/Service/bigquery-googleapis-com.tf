resource "google_project_service" "bigquery_googleapis_com" {
  project = var.gcp_project_id
  service = "bigquery.googleapis.com"
}
# terraform import google_project_service.bigquery_googleapis_com 924197226133/bigquery.googleapis.com
