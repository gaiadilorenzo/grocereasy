resource "google_bigquery_dataset" "supermarket" {
  access {
    role          = "OWNER"
    special_group = "projectOwners"
  }

  access {
    role          = "READER"
    special_group = "projectReaders"
  }

  access {
    role          = "WRITER"
    special_group = "projectWriters"
  }

  dataset_id                      = "supermarket"
  default_partition_expiration_ms = 2592000000
  default_table_expiration_ms     = 2592000000
  delete_contents_on_destroy      = false
  description                     = "A dataset containing all the data collected from supermarkets."
  location                        = "US"
  project                         =  var.gcp_project_id
}
# terraform import google_bigquery_dataset.supermarket projects/${var.gcp_project_id}/datasets/supermarket
