resource "google_pubsub_topic" "dead" {
  name    = "dead"
  project = var.gcp_project_id
}
# terraform import google_pubsub_topic.dead projects/${var.gcp_project_id}/topics/dead
