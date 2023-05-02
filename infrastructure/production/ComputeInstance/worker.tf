resource "google_compute_instance" "worker" {
  boot_disk {
    auto_delete = true
    device_name = "worker"

    initialize_params {
      image = "https://www.googleapis.com/compute/beta/projects/cos-cloud/global/images/cos-stable-101-17162-127-8"
      size  = 10
      type  = "pd-standard"
    }

    mode   = "READ_WRITE"
    source = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/zones/us-central1-c/disks/worker"
  }

  confidential_instance_config {
    enable_confidential_compute = false
  }

  labels = {
    container-vm = "cos-stable-101-17162-127-8"
  }

  machine_type = "e2-micro"

  metadata = {
    gce-container-declaration = "# DISCLAIMER:\n# This container declaration format is not a public API and may change without\n# notice. Please use gcloud command-line tool or Google Cloud Console to run\n# Containers on Google Compute Engine.\n\nspec:\n  containers:\n  - image: gcr.io/${var.gcp_project_id}/worker:62e581acc7b38286356b2c8808436fd8f1691756\n    name: worker\n    stdin: false\n    tty: false\n    volumeMounts: []\n  restartPolicy: Always\n  volumes: []\n"
    startup-script            = "#! /bin/bash\n    docker image prune -af"
  }

  name = "worker"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    network            = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/global/networks/default"
    network_ip         = "10.128.0.4"
    stack_type         = "IPV4_ONLY"
    subnetwork         = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/regions/us-central1/subnetworks/default"
    subnetwork_project = var.gcp_project_id
  }

  project = var.gcp_project_id

  reservation_affinity {
    type = "ANY_RESERVATION"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "deploy@${var.gcp_project_id}.iam.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = var.gcp_zone
}
# terraform import google_compute_instance.worker projects/${var.gcp_project_id}/zones/us-central1-c/instances/worker
