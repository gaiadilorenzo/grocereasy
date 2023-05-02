resource "google_pubsub_topic" "storer_completed" {
  message_retention_duration = "86600s"
  name                       = "storer_completed"
  project                    = var.gcp_project_id
}
# terraform import google_pubsub_topic.storer_completed projects/${var.gcp_project_id}/topics/storer_completed
