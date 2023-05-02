resource "google_pubsub_subscription" "worker_completed" {
  ack_deadline_seconds = 600

  dead_letter_policy {
    dead_letter_topic     = "projects/${var.gcp_project_id}/topics/dead"
    max_delivery_attempts = 5
  }

  enable_exactly_once_delivery = true
  enable_message_ordering      = true

  expiration_policy {
    ttl = "2678400s"
  }

  message_retention_duration = "604800s"
  name                       = "worker_completed"
  project                    = var.gcp_project_id
  topic                      = "projects/${var.gcp_project_id}/topics/worker_completed"
}
# terraform import google_pubsub_subscription.worker_completed projects/${var.gcp_project_id}/subscriptions/worker_completed
