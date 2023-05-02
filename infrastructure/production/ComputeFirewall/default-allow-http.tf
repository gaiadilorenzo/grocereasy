resource "google_compute_firewall" "default_allow_http" {
  allow {
    ports    = ["80"]
    protocol = "tcp"
  }

  direction     = "INGRESS"
  name          = "default-allow-http"
  network       = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/global/networks/default"
  priority      = 1000
  project       = var.gcp_project_id
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}
# terraform import google_compute_firewall.default_allow_http projects/${var.gcp_project_id}/global/firewalls/default-allow-http
