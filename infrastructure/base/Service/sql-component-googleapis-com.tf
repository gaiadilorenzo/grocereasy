resource "google_project_service" "sql_component_googleapis_com" {
  project = var.gcp_project_id
  service = "sql-component.googleapis.com"
}
# terraform import google_project_service.sql_component_googleapis_com 924197226133/sql-component.googleapis.com
