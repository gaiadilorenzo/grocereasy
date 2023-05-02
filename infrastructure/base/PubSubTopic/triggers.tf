resource "google_pubsub_topic" "triggers" {
  message_retention_duration = "86600s"
  name                       = "triggers"
  project                    = var.gcp_project_id
}
# terraform import google_pubsub_topic.triggers projects/${var.gcp_project_id}/topics/triggers
