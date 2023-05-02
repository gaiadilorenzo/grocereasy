resource "google_storage_bucket" "artifacts_appspot_com" {
  force_destroy            = false
  location                 = "US"
  name                     = "artifacts.${var.gcp_project_id}.appspot.com"
  project                  = var.gcp_project_id
  public_access_prevention = "inherited"
  storage_class            = "STANDARD"
}
# terraform import google_storage_bucket.artifacts_grocereasy_360206_appspot_com artifacts.${var.gcp_project_id}.appspot.com
