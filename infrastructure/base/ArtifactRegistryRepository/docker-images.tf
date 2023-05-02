resource "google_artifact_registry_repository" "docker_images" {
  description   = "Docker repository for Groceareasy."
  format        = "DOCKER"
  location      = "us-central1"
  project       = var.gcp_project_id
  repository_id = "docker-images"
}
# terraform import google_artifact_registry_repository.docker_images projects/${var.gcp_project_id}/locations/us-central1/repositories/docker-images
