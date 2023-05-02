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
}


resource "google_service_account" "tester" {
  account_id   = "tester"
  display_name = "Test Service Account"
  project      = var.gcp_project_id
}
# terraform import google_service_account.tester projects/${var.gcp_project_id}/serviceAccounts/tester@${var.gcp_project_id}.iam.gserviceaccount.com


resource "google_bigquery_dataset_access" "jobs_tester" {
  dataset_id    = google_bigquery_dataset.jobs.dataset_id
  project       = var.gcp_project_id
  role          = "WRITER"
  user_by_email = google_service_account.tester.email
}

resource "google_bigquery_dataset_access" "superamrket_tester" {
  dataset_id    = google_bigquery_dataset.supermarket.dataset_id
  project       = var.gcp_project_id
  role          = "WRITER"
  user_by_email = google_service_account.tester.email
}