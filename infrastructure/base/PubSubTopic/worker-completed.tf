resource "google_pubsub_topic" "worker_completed" {
  message_retention_duration = "86600s"
  name                       = "worker_completed"
  project                    = var.gcp_project_id
}
# terraform import google_pubsub_topic.worker_completed projects/${var.gcp_project_id}/topics/worker_completed
