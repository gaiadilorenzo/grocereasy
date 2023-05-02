resource "google_project_service" "pubsub_googleapis_com" {
  project = var.gcp_project_id
  service = "pubsub.googleapis.com"
}
# terraform import google_project_service.pubsub_googleapis_com 924197226133/pubsub.googleapis.com
