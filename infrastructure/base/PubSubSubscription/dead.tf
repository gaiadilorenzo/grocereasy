resource "google_pubsub_subscription" "dead" {
  ack_deadline_seconds       = 10
  message_retention_duration = "604800s"
  name                       = "dead"
  project                    = var.gcp_project_id
  topic                      = "projects/${var.gcp_project_id}/topics/dead"
}
# terraform import google_pubsub_subscription.dead projects/${var.gcp_project_id}/subscriptions/dead
