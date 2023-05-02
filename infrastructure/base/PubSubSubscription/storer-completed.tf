resource "google_pubsub_subscription" "storer_completed" {
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
  name                       = "storer_completed"
  project                    = var.gcp_project_id

  retry_policy {
    maximum_backoff = "600s"
    minimum_backoff = "10s"
  }

  topic = "projects/${var.gcp_project_id}/topics/storer_completed"
}
# terraform import google_pubsub_subscription.storer_completed projects/${var.gcp_project_id}/subscriptions/storer_completed
