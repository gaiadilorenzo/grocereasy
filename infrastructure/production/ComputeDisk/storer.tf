resource "google_compute_disk" "storer" {
  image                     = "https://www.googleapis.com/compute/beta/projects/cos-cloud/global/images/cos-stable-101-17162-127-8"
  name                      = "storer"
  physical_block_size_bytes = 4096
  project                   = var.gcp_project_id
  size                      = 10
  type                      = "pd-standard"
  zone                      = var.gcp_zone
}
# terraform import google_compute_disk.storer projects/${var.gcp_project_id}/zones/us-central1-c/disks/storer
