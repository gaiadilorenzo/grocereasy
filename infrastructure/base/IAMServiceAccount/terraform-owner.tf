resource "google_service_account" "terraform_owner" {
  account_id   = "terraform-owner"
  display_name = "Terraform owner"
  project      = var.gcp_project_id
}
# terraform import google_service_account.terraform_owner projects/${var.gcp_project_id}/serviceAccounts/terraform-owner@${var.gcp_project_id}.iam.gserviceaccount.com
