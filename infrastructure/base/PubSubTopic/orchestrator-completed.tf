resource "google_pubsub_topic" "orchestrator_completed" {
  message_retention_duration = "86600s"
  name                       = "orchestrator_completed"
  project                    = var.gcp_project_id
}
# terraform import google_pubsub_topic.orchestrator_completed projects/${var.gcp_project_id}/topics/orchestrator_completed
