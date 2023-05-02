resource "google_bigquery_table" "jobs" {
  dataset_id = "jobs"
  project    = var.gcp_project_id
  schema     = "[{\"description\":\"The name of the supermarket.\",\"mode\":\"REQUIRED\",\"name\":\"supermarket\",\"type\":\"STRING\"},{\"description\":\"The ID of the item.\",\"mode\":\"REQUIRED\",\"name\":\"url\",\"type\":\"STRING\"},{\"description\":\"The timestamp of the insertion.\",\"mode\":\"REQUIRED\",\"name\":\"timestamp\",\"type\":\"TIMESTAMP\"},{\"description\":\"The timestamp of the last execution.\",\"mode\":\"NULLABLE\",\"name\":\"last_executed\",\"type\":\"TIMESTAMP\"}]"
  table_id   = "jobs"

  time_partitioning {
    expiration_ms = 5184000000
    field         = "timestamp"
    type          = "HOUR"
  }
}
# terraform import google_bigquery_table.jobs projects/${var.gcp_project_id}/datasets/jobs/tables/jobs
