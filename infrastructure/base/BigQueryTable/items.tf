resource "google_bigquery_table" "items" {
  clustering  = ["product"]
  dataset_id  = "supermarket"
  description = "Table storing all supermarket items."
  project     = var.gcp_project_id
  schema      = "[{\"description\":\"The name of the item.\",\"mode\":\"REQUIRED\",\"name\":\"name\",\"type\":\"STRING\"},{\"description\":\"The ID of the item.\",\"mode\":\"REQUIRED\",\"name\":\"id\",\"type\":\"STRING\"},{\"description\":\"The supermarket of the item.\",\"mode\":\"REQUIRED\",\"name\":\"supermarket\",\"type\":\"STRING\"},{\"description\":\"The category of the item.\",\"mode\":\"REQUIRED\",\"name\":\"product\",\"type\":\"STRING\"},{\"description\":\"The brand of the item.\",\"mode\":\"REQUIRED\",\"name\":\"brand\",\"type\":\"STRING\"},{\"description\":\"The price of the item.\",\"mode\":\"REQUIRED\",\"name\":\"price\",\"type\":\"FLOAT\"},{\"description\":\"The dimension of the item.\",\"mode\":\"REQUIRED\",\"name\":\"quantity\",\"type\":\"FLOAT\"},{\"description\":\"The timestamp of the insertion.\",\"mode\":\"REQUIRED\",\"name\":\"timestamp\",\"type\":\"TIMESTAMP\"},{\"description\":\"The link of the item.\",\"mode\":\"NULLABLE\",\"name\":\"link\",\"type\":\"STRING\"},{\"description\":\"The rank of the item.\",\"mode\":\"NULLABLE\",\"name\":\"rank\",\"type\":\"INTEGER\"},{\"description\":\"The offer on the item.\",\"mode\":\"NULLABLE\",\"name\":\"offer\",\"type\":\"STRING\"}]"
  table_id    = "items"
}
# terraform import google_bigquery_table.items projects/${var.gcp_project_id}/datasets/supermarket/tables/items
