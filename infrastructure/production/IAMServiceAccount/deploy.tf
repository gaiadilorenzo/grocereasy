locals {
  datasets = {
    supermarket = {
      dataset_id  = "supermarket",
      description = "A dataset containing all the data collected from supermarkets."
    },
    jobs = {
      dataset_id  = "jobs",
      description = "A dataset containing all the data related to jobs."
    },
  }

  topics = [
    "orchestrator_completed",
    "worker_completed",
    "storer_completed"
  ]

  subscriptions = [
    "triggers",
    "orchestrator_completed",
    "worker_completed",
  ]
}

resource "google_service_account" "deploy" {
  account_id   = "deploy"
  display_name = "Deploy"
  project      = var.gcp_project_id
}
# terraform import google_service_account.deploy projects/${var.gcp_project_id}/serviceAccounts/deploy@${var.gcp_project_id}.iam.gserviceaccount.com

resource "google_bigquery_dataset_access" "jobs_deployr" {
  dataset_id    = google_bigquery_dataset.jobs.dataset_id
  project       = var.gcp_project_id
  role          = "WRITER"
  user_by_email = google_service_account.deploy.email
}

resource "google_bigquery_dataset_access" "superamrket_deploy" {
  dataset_id    = google_bigquery_dataset.supermarket.dataset_id
  project       = var.gcp_project_id
  role          = "WRITER"
  user_by_email = google_service_account.deploy.email
}

resource "google_pubsub_subscription_iam_member" "iam_subscriptions" {
  for_each = locals.subscriptions

  subscription = each.value
  role         = "roles/pubsub.subscriber"
  member       = "serviceAccount:${google_service_account.deploy.email}"
  project      = var.gcp_project_id

  depends_on = [google_pubsub_subscription.pubsub_subscription]
}

resource "google_pubsub_topic_iam_member" "iam_topics" {
  for_each = locals.value

  topic   = each.value
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.deploy.email}"
  project = var.gcp_project_id

  depends_on = [google_pubsub_topic.pubsub_topic]
}