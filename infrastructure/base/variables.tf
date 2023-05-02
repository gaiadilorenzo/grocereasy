variable "gcp_project_id" {
  type        = string
  description = "The GCP Project ID."
}

variable "gcp_zone" {
  type        = string
  description = "The GCP Project zone."
  default = var.gcp_zone
}
